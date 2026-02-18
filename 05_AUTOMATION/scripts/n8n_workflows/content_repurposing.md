# Content Repurposing Workflow

**Purpose:** Monitor RSS feeds, extract key points with Claude, generate platform-specific social posts, queue for human approval, then post.

**Workflow ID:** `content_repurposing_v1`
**Trigger:** Schedule (every 4 hours) or webhook
**Est. Run Time:** 2-5 minutes per article

---

## Architecture Overview

```
RSS Feed Monitor
       |
       v
New Article Detected
       |
       v
Claude: Extract Key Points
       |
       v
Generate Posts (X, LinkedIn, Reddit)
       |
       v
Queue in Google Sheets (LEDGER/CONTENT_PIPELINE.csv)
       |
       v
Human Reviews & Approves
       |
       v
Post to Buffer/Native Schedulers
```

---

## Node Configuration

### Node 1: Schedule Trigger
**Type:** `n8n-nodes-base.scheduleTrigger`
**Purpose:** Run workflow every 4 hours

```json
{
  "rule": {
    "interval": [{"field": "hours", "triggerAtHour": 4}]
  }
}
```

**Configuration:**
- Run at: 6am, 10am, 2pm, 6pm, 10pm (peak engagement times)
- Skip weekends: false (content runs 7 days)

---

### Node 2: RSS Feed Read
**Type:** `n8n-nodes-base.rssFeedRead`
**Purpose:** Pull new articles from monitored feeds

```json
{
  "urls": [
    "https://indiehackers.com/feed",
    "https://bensbites.co/feed",
    "https://tldr.tech/feed",
    "{{ $env.CUSTOM_RSS_FEEDS }}"
  ],
  "options": {
    "ignoreSSLIssues": false
  }
}
```

**Output:** Array of articles with title, link, description, pubDate

---

### Node 3: Filter New Items
**Type:** `n8n-nodes-base.filter`
**Purpose:** Only process articles from last 4 hours

```json
{
  "conditions": {
    "dateTime": [
      {
        "value1": "={{ $json.pubDate }}",
        "operation": "isAfter",
        "value2": "={{ $now.minus({hours: 4}).toISO() }}"
      }
    ]
  }
}
```

---

### Node 4: Check Duplicates (Google Sheets)
**Type:** `n8n-nodes-base.googleSheets`
**Purpose:** Check if article already processed

```json
{
  "operation": "lookup",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "CONTENT_PIPELINE",
  "lookupColumn": "source_url",
  "lookupValue": "={{ $json.link }}"
}
```

**Logic:** If found, skip. If not found, continue.

---

### Node 5: Claude - Extract Key Points
**Type:** `n8n-nodes-base.httpRequest`
**Purpose:** Call Claude API to extract actionable insights

```json
{
  "method": "POST",
  "url": "https://api.anthropic.com/v1/messages",
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "anthropicApi",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {"name": "anthropic-version", "value": "2023-06-01"},
      {"name": "x-api-key", "value": "{{ $env.ANTHROPIC_API_KEY }}"}
    ]
  },
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {
        "name": "model",
        "value": "claude-3-haiku-20240307"
      },
      {
        "name": "max_tokens",
        "value": 1024
      },
      {
        "name": "messages",
        "value": "[{\"role\": \"user\", \"content\": \"Extract 3 key actionable insights from this article. Be specific with numbers and tactics. No fluff.\\n\\nTitle: {{ $json.title }}\\n\\nContent: {{ $json.description }}\"}]"
      }
    ]
  }
}
```

**Cost:** ~$0.001 per article (Haiku)

---

### Node 6: Claude - Generate Platform Posts
**Type:** `n8n-nodes-base.httpRequest`
**Purpose:** Generate platform-specific posts from key points

```json
{
  "method": "POST",
  "url": "https://api.anthropic.com/v1/messages",
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {
        "name": "model",
        "value": "claude-3-haiku-20240307"
      },
      {
        "name": "max_tokens",
        "value": 2048
      },
      {
        "name": "system",
        "value": "You write like @levelsio - direct, specific numbers, no fluff. Never use em dashes. Never use words like leverage, utilize, comprehensive, robust, innovative, seamless."
      },
      {
        "name": "messages",
        "value": "[{\"role\": \"user\", \"content\": \"Create 3 social posts from these insights:\\n\\n{{ $node['Claude - Extract Key Points'].json.content[0].text }}\\n\\nFormat:\\n1. X/Twitter (280 chars, hook first, no hashtags)\\n2. LinkedIn (300 chars, professional but not corporate)\\n3. Reddit title + body (for r/SideProject or r/EntrepreneurRideAlong)\\n\\nOutput as JSON with keys: x_post, linkedin_post, reddit_title, reddit_body\"}]"
      }
    ]
  }
}
```

---

### Node 7: Parse Claude Response
**Type:** `n8n-nodes-base.code`
**Purpose:** Extract JSON posts from Claude response

```javascript
const response = $input.first().json.content[0].text;

// Try to parse JSON from response
let posts;
try {
  // Find JSON in response
  const jsonMatch = response.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    posts = JSON.parse(jsonMatch[0]);
  } else {
    throw new Error('No JSON found in response');
  }
} catch (e) {
  // Fallback: create placeholder
  posts = {
    x_post: 'MANUAL_REVIEW_NEEDED',
    linkedin_post: 'MANUAL_REVIEW_NEEDED',
    reddit_title: 'MANUAL_REVIEW_NEEDED',
    reddit_body: 'MANUAL_REVIEW_NEEDED'
  };
}

return [{
  json: {
    ...posts,
    source_title: $('RSS Feed Read').first().json.title,
    source_url: $('RSS Feed Read').first().json.link,
    source_date: $('RSS Feed Read').first().json.pubDate,
    generated_at: new Date().toISOString(),
    status: 'PENDING_REVIEW'
  }
}];
```

---

### Node 8: Add to Approval Queue (Google Sheets)
**Type:** `n8n-nodes-base.googleSheets`
**Purpose:** Queue posts for human review

```json
{
  "operation": "append",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "CONTENT_PIPELINE",
  "columns": {
    "mappingMode": "defineBelow",
    "value": {
      "source_title": "={{ $json.source_title }}",
      "source_url": "={{ $json.source_url }}",
      "x_post": "={{ $json.x_post }}",
      "linkedin_post": "={{ $json.linkedin_post }}",
      "reddit_title": "={{ $json.reddit_title }}",
      "reddit_body": "={{ $json.reddit_body }}",
      "status": "PENDING_REVIEW",
      "generated_at": "={{ $json.generated_at }}",
      "approved_at": "",
      "posted_at": ""
    }
  }
}
```

---

### Node 9: Notify for Review (Slack/Email)
**Type:** `n8n-nodes-base.slack` or `n8n-nodes-base.emailSend`
**Purpose:** Alert when new posts ready for review

```json
{
  "channel": "#content-queue",
  "text": "New content ready for review:\n\nSource: {{ $json.source_title }}\n\nX Post:\n{{ $json.x_post }}\n\nReview at: {{ $env.SHEETS_URL }}"
}
```

---

## Human Approval Workflow (Separate)

### Trigger: Google Sheets Update
When `status` column changes from `PENDING_REVIEW` to `APPROVED`:

### Node A: Get Approved Row
```json
{
  "operation": "read",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "CONTENT_PIPELINE",
  "range": "A:Z",
  "filters": {
    "status": "APPROVED",
    "posted_at": ""
  }
}
```

### Node B: Post to Buffer (X/Twitter)
**Type:** `n8n-nodes-base.httpRequest`
```json
{
  "method": "POST",
  "url": "https://api.bufferapp.com/1/updates/create.json",
  "authentication": "predefinedCredentialType",
  "nodeCredentialType": "bufferApi",
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {"name": "text", "value": "={{ $json.x_post }}"},
      {"name": "profile_ids[]", "value": "{{ $env.BUFFER_X_PROFILE_ID }}"},
      {"name": "scheduled_at", "value": "={{ $now.plus({hours: 2}).toISO() }}"}
    ]
  }
}
```

### Node C: Post to LinkedIn (Native API)
**Type:** `n8n-nodes-base.httpRequest`
```json
{
  "method": "POST",
  "url": "https://api.linkedin.com/v2/ugcPosts",
  "authentication": "oAuth2Api",
  "sendHeaders": true,
  "headerParameters": {
    "parameters": [
      {"name": "X-Restli-Protocol-Version", "value": "2.0.0"}
    ]
  },
  "sendBody": true,
  "bodyParameters": {
    "parameters": [
      {
        "name": "author",
        "value": "urn:li:person:{{ $env.LINKEDIN_PERSON_ID }}"
      },
      {
        "name": "lifecycleState",
        "value": "PUBLISHED"
      },
      {
        "name": "specificContent",
        "value": "{\"com.linkedin.ugc.ShareContent\":{\"shareCommentary\":{\"text\":\"{{ $json.linkedin_post }}\"},\"shareMediaCategory\":\"NONE\"}}"
      },
      {
        "name": "visibility",
        "value": "{\"com.linkedin.ugc.MemberNetworkVisibility\":\"PUBLIC\"}"
      }
    ]
  }
}
```

### Node D: Update Posted Status
```json
{
  "operation": "update",
  "documentId": "{{ $env.LEDGER_SHEET_ID }}",
  "sheetName": "CONTENT_PIPELINE",
  "dataMode": "autoMapInputData",
  "columns": {
    "posted_at": "={{ $now.toISO() }}",
    "status": "POSTED"
  }
}
```

---

## Required Credentials

| Credential | Purpose | Setup Location |
|------------|---------|----------------|
| `anthropicApi` | Claude API calls | n8n Credentials > Anthropic |
| `googleSheetsOAuth2Api` | Sheet read/write | n8n Credentials > Google Sheets |
| `bufferApi` | Post scheduling | n8n Credentials > Buffer |
| `linkedInOAuth2Api` | LinkedIn posting | n8n Credentials > LinkedIn |
| `slackApi` | Notifications | n8n Credentials > Slack |

---

## Environment Variables

```bash
ANTHROPIC_API_KEY=sk-ant-...
LEDGER_SHEET_ID=1abc...xyz
BUFFER_X_PROFILE_ID=profile_id
LINKEDIN_PERSON_ID=person_id
SHEETS_URL=https://docs.google.com/spreadsheets/d/...
```

---

## Error Handling

### On Claude API Error
- Retry 3 times with exponential backoff
- If still fails, log to `CONTENT_PIPELINE` with status `GENERATION_FAILED`
- Alert via Slack

### On Sheet Write Error
- Retry once
- If fails, save to local JSON backup
- Alert via Slack

### On Post Failure
- Log error to sheet
- Set status to `POST_FAILED`
- Do not retry automatically (may need credential refresh)

---

## Cost Estimation

| Component | Cost/Month (100 articles) |
|-----------|---------------------------|
| Claude Haiku (extraction) | $0.10 |
| Claude Haiku (generation) | $0.20 |
| Buffer | Free tier (3 channels) |
| n8n Cloud | $20/month or self-hosted |
| **Total** | ~$20-25/month |

---

## Testing Checklist

- [ ] RSS feeds return articles
- [ ] Duplicate detection works
- [ ] Claude extracts coherent key points
- [ ] Generated posts follow style guide (no em dashes, no banned words)
- [ ] Posts save to Google Sheets correctly
- [ ] Notification sends to Slack
- [ ] Manual approval workflow triggers posting
- [ ] All platforms receive posts
- [ ] Posted status updates correctly

---

## Maintenance

**Weekly:**
- Review post performance in analytics
- Adjust prompts if quality drops
- Check for RSS feed changes

**Monthly:**
- Refresh OAuth tokens if needed
- Review cost vs. output
- Add/remove RSS sources based on signal quality
