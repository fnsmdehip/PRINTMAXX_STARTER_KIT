# n8n Workflow Automation

Self-hosted automation workflows for content farm operations. Build once, run forever.

---

## Why n8n?

| Feature | n8n | Zapier | Make |
|---------|-----|--------|------|
| Self-hosted | Yes | No | No |
| Monthly cost | $0-20 | $20-100+ | $9-50+ |
| Executions | Unlimited | Limited | Limited |
| Complexity | High | Low | Medium |
| Learning curve | Steep | Easy | Medium |

**Bottom line:** n8n is free/cheap and has no execution limits. Worth the setup time for content farms.

---

## Setup requirements

### Self-hosting options

**Option 1: Local machine**
```bash
# Using Docker
docker run -it --rm \
  --name n8n \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```
Cost: $0
Best for: Testing

**Option 2: VPS hosting**
- DigitalOcean Droplet: $6/month
- Hetzner VPS: $4/month
- AWS Lightsail: $5/month

**Option 3: n8n Cloud**
- Starter: $20/month
- Best for: Simplicity

### Required integrations

API keys needed:
- OpenAI (content generation)
- Twitter/X API (posting)
- Google Sheets (data storage)
- Airtable (alternative storage)
- Telegram/Discord (notifications)

---

## Workflow 1: Content idea generator

**Purpose:** Generate content ideas weekly and store in database

### Trigger
```
Schedule: Every Sunday at 9pm
```

### Steps

1. **HTTP Request - Get trending topics**
```json
{
  "url": "https://api.twitter.com/2/tweets/search/recent",
  "params": {
    "query": "[niche] min_retweets:100",
    "max_results": 50
  }
}
```

2. **OpenAI - Generate ideas**
```json
{
  "model": "gpt-4",
  "prompt": "Based on these trending tweets, generate 20 content ideas for [niche]:\n\n{{trending_tweets}}\n\nFormat: Title | Hook | Content type"
}
```

3. **Google Sheets - Store ideas**
```json
{
  "spreadsheetId": "YOUR_SHEET_ID",
  "range": "Ideas!A:D",
  "values": "{{generated_ideas}}"
}
```

4. **Telegram - Notify**
```json
{
  "chatId": "YOUR_CHAT_ID",
  "text": "20 new content ideas generated for the week!"
}
```

### Output
- 20 fresh content ideas per week
- Stored in Google Sheets for team access
- Notification sent when complete

---

## Workflow 2: Auto-generate content drafts

**Purpose:** Turn content ideas into full drafts

### Trigger
```
Webhook: When new idea marked "Ready" in Sheets
```

### Steps

1. **Google Sheets - Get idea**
```json
{
  "spreadsheetId": "YOUR_SHEET_ID",
  "range": "Ideas!A:E",
  "filter": "status = 'Ready'"
}
```

2. **OpenAI - Generate draft**
```json
{
  "model": "gpt-4",
  "prompt": "Create a [content_type] about: {{idea_title}}\n\nHook: {{hook}}\n\nRequirements:\n- Under 280 characters for Twitter\n- Include call-to-action\n- Match voice: [your voice description]"
}
```

3. **IF - Route by platform**
```
Twitter → Twitter formatting node
Instagram → Instagram formatting node
TikTok → TikTok script formatting
YouTube → YouTube script formatting
```

4. **Google Sheets - Store draft**
```json
{
  "spreadsheetId": "YOUR_SHEET_ID",
  "range": "Drafts!A:F",
  "values": [
    "{{platform}}",
    "{{draft}}",
    "{{hashtags}}",
    "{{scheduled_time}}",
    "Pending review"
  ]
}
```

### Output
- Platform-specific formatted content
- Stored for review before posting
- Human reviews and approves

---

## Workflow 3: Scheduled posting (X/Twitter)

**Purpose:** Auto-post approved content to Twitter

### Trigger
```
Schedule: Every hour at :00
```

### Steps

1. **Google Sheets - Get scheduled posts**
```json
{
  "filter": "status = 'Approved' AND scheduled_time <= NOW()"
}
```

2. **Loop - For each post**

3. **Twitter API - Post tweet**
```json
{
  "endpoint": "tweets",
  "method": "POST",
  "body": {
    "text": "{{post_content}}"
  }
}
```

4. **Google Sheets - Update status**
```json
{
  "update": {
    "status": "Posted",
    "tweet_id": "{{response.id}}",
    "posted_at": "{{NOW()}}"
  }
}
```

5. **Error handling**
```
IF error:
  - Mark as "Failed"
  - Log error message
  - Send Telegram alert
```

### Output
- Automated posting at scheduled times
- Status tracking in Sheets
- Error notifications

---

## Workflow 4: Engagement monitoring

**Purpose:** Track engagement and surface top performers

### Trigger
```
Schedule: Every 6 hours
```

### Steps

1. **Google Sheets - Get recent posts**
```json
{
  "filter": "posted_at > 24_hours_ago"
}
```

2. **Twitter API - Get metrics**
```json
{
  "endpoint": "tweets",
  "ids": "{{tweet_ids}}",
  "tweet.fields": "public_metrics"
}
```

3. **Code - Calculate engagement rate**
```javascript
const engagementRate = (likes + retweets + replies) / impressions * 100;
const isTopPerformer = engagementRate > 5; // 5% threshold
return { engagementRate, isTopPerformer };
```

4. **Google Sheets - Update metrics**
```json
{
  "update": {
    "impressions": "{{metrics.impressions}}",
    "likes": "{{metrics.likes}}",
    "retweets": "{{metrics.retweets}}",
    "engagement_rate": "{{engagementRate}}"
  }
}
```

5. **IF - Top performer alert**
```
IF isTopPerformer:
  Send Telegram: "Top performer! {{post_content}} - {{engagementRate}}%"
```

### Output
- Hourly metric updates
- Top performer identification
- Alerts for viral content

---

## Workflow 5: Content repurposing

**Purpose:** Convert one piece of content to multiple platforms

### Trigger
```
Webhook: When content marked "Repurpose" in Sheets
```

### Steps

1. **Get original content**
```json
{
  "source": "Original content from any platform"
}
```

2. **OpenAI - Generate variations**
```json
{
  "prompts": [
    "Convert to Twitter thread (5 tweets):",
    "Convert to Instagram caption:",
    "Convert to TikTok script (15 seconds):",
    "Convert to YouTube Shorts script:"
  ]
}
```

3. **Split - Create multiple items**
```
Twitter variation → Twitter queue
Instagram variation → Instagram queue
TikTok variation → TikTok queue
YouTube variation → YouTube queue
```

4. **Google Sheets - Add to queues**
```json
{
  "add_to_sheets": [
    { "sheet": "Twitter_Queue", "content": "{{twitter_version}}" },
    { "sheet": "Instagram_Queue", "content": "{{instagram_version}}" },
    { "sheet": "TikTok_Queue", "content": "{{tiktok_version}}" },
    { "sheet": "YouTube_Queue", "content": "{{youtube_version}}" }
  ]
}
```

### Output
- One piece of content → 4 platform versions
- Each added to respective queue
- Ready for review and scheduling

---

## Workflow 6: Lead capture processor

**Purpose:** Process leads from bio links and DMs

### Trigger
```
Webhook: From Stan Store / Linktree / Form submission
```

### Steps

1. **Parse webhook data**
```json
{
  "email": "{{body.email}}",
  "source": "{{body.source}}",
  "lead_magnet": "{{body.product}}"
}
```

2. **Google Sheets - Add to leads**
```json
{
  "spreadsheetId": "YOUR_SHEET_ID",
  "range": "Leads!A:E",
  "values": [
    "{{email}}",
    "{{source}}",
    "{{lead_magnet}}",
    "{{timestamp}}",
    "New"
  ]
}
```

3. **Email - Send lead magnet**
```json
{
  "to": "{{email}}",
  "subject": "Here's your {{lead_magnet}}",
  "body": "{{lead_magnet_email_template}}"
}
```

4. **Add to email sequence**
```json
{
  "add_to_sequence": "Welcome sequence",
  "email": "{{email}}"
}
```

### Output
- Lead captured in database
- Lead magnet delivered
- Added to nurture sequence

---

## Workflow 7: Competitor monitoring

**Purpose:** Track competitor content and performance

### Trigger
```
Schedule: Daily at 6am
```

### Steps

1. **HTTP Request - Get competitor posts**
```json
{
  "twitter_accounts": ["@competitor1", "@competitor2"],
  "get_last_24h_posts": true
}
```

2. **OpenAI - Analyze content**
```json
{
  "prompt": "Analyze these competitor posts. Identify:\n1. Topics that got high engagement\n2. Content formats used\n3. Hooks that worked\n4. Gaps we could fill\n\nPosts: {{competitor_posts}}"
}
```

3. **Google Sheets - Store analysis**
```json
{
  "sheet": "Competitor_Intel",
  "data": "{{analysis}}"
}
```

4. **IF - High performer detected**
```
IF competitor_post.engagement > threshold:
  Add to "Content_Inspiration" sheet
```

### Output
- Daily competitor analysis
- High-performing content flagged
- Content gaps identified

---

## Workflow 8: Weekly analytics report

**Purpose:** Compile weekly performance summary

### Trigger
```
Schedule: Every Monday at 8am
```

### Steps

1. **Google Sheets - Get last week's posts**
```json
{
  "filter": "posted_at BETWEEN last_monday AND last_sunday"
}
```

2. **Code - Calculate metrics**
```javascript
const totalImpressions = posts.reduce((sum, p) => sum + p.impressions, 0);
const totalEngagement = posts.reduce((sum, p) => sum + p.engagement, 0);
const avgEngagementRate = totalEngagement / totalImpressions * 100;
const topPosts = posts.sort((a, b) => b.engagement - a.engagement).slice(0, 5);
const followerGrowth = currentFollowers - lastWeekFollowers;

return {
  totalImpressions,
  totalEngagement,
  avgEngagementRate,
  topPosts,
  followerGrowth,
  postsPublished: posts.length
};
```

3. **Generate report**
```json
{
  "template": "weekly_report",
  "data": {
    "period": "{{last_week}}",
    "posts": "{{postsPublished}}",
    "impressions": "{{totalImpressions}}",
    "engagement_rate": "{{avgEngagementRate}}%",
    "follower_growth": "+{{followerGrowth}}",
    "top_posts": "{{topPosts}}"
  }
}
```

4. **Send report**
```
- Email to self
- Post to Slack/Discord
- Save to Google Drive
```

### Output
- Weekly performance summary
- Top performing content identified
- Growth trends tracked

---

## Workflow templates

### Template structure

Each workflow should include:
```
1. Clear trigger definition
2. Input validation
3. Main processing logic
4. Error handling
5. Success notification
6. Logging
```

### Error handling pattern

```json
{
  "try": {
    "main_workflow_steps": "..."
  },
  "catch": {
    "log_error": {
      "sheet": "Error_Log",
      "error": "{{error.message}}",
      "workflow": "{{workflow_name}}",
      "timestamp": "{{NOW()}}"
    },
    "notify": {
      "telegram": "Workflow {{workflow_name}} failed: {{error.message}}"
    }
  }
}
```

---

## Implementation checklist

### Phase 1: Foundation (Week 1)
- [ ] Set up n8n (self-hosted or cloud)
- [ ] Configure Google Sheets as database
- [ ] Set up API connections
- [ ] Create error logging workflow
- [ ] Test notification channels

### Phase 2: Content pipeline (Week 2)
- [ ] Build content idea generator
- [ ] Build draft generator
- [ ] Build scheduling workflow
- [ ] Test end-to-end flow

### Phase 3: Monitoring (Week 3)
- [ ] Build engagement monitoring
- [ ] Build competitor tracking
- [ ] Build weekly report
- [ ] Set up alerts

### Phase 4: Optimization (Week 4)
- [ ] Build repurposing workflow
- [ ] Build lead processor
- [ ] Optimize all workflows
- [ ] Document everything

---

## Cost summary

**Self-hosted setup:**
- VPS: $5/month
- Domain (optional): $10/year
- APIs: Variable (most have free tiers)

**Total: ~$5-20/month**

Compare to:
- Zapier: $50-200/month at scale
- Make: $30-100/month at scale

**Annual savings: $500-2,000+**
