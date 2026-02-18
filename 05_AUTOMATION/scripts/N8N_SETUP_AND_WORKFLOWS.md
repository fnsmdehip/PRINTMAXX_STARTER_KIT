# n8n Self-Hosted Setup + First Workflows

**Created:** 2026-02-03
**Priority:** 9.0 (replaces $100-300/mo SaaS stack, MCP integration ready)
**MEGA_RALPH:** EX-04 Day 4 Iteration 14

---

## Why n8n

n8n is an open-source workflow automation tool with 169.6K GitHub stars. Self-hosted = free. Replaces Buffer, Zapier, Make.com, and custom Python scripts.

Key advantages for PRINTMAXX:
- **Free self-hosted** (vs Buffer $12/mo + Zapier $30/mo + Make $9/mo = $51/mo saved)
- **MCP integration** (ALPHA497) - connects to Claude, model context protocol servers
- **1,400+ integrations** - Twitter/X, Reddit, Beehiiv, Gumroad, Stripe, Google Sheets
- **Visual workflow builder** - no code for simple flows, code nodes for complex logic
- **Self-hosted data** - no third-party storing our content or credentials
- **Webhook triggers** - responds to events in real-time

---

## Docker Setup (10 minutes)

### Prerequisites
- Docker Desktop installed (free)
- 2GB RAM minimum (4GB recommended)

### docker-compose.yml

Create at `AUTOMATIONS/n8n/docker-compose.yml`:

```yaml
version: '3.8'

services:
  n8n:
    image: docker.n8n.io/n8nio/n8n
    restart: always
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=printmaxx
      - N8N_BASIC_AUTH_PASSWORD=${N8N_PASSWORD}
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - GENERIC_TIMEZONE=America/New_York
      - N8N_SECURE_COOKIE=false
      - N8N_RUNNERS_ENABLED=true
    volumes:
      - n8n_data:/home/node/.n8n
    networks:
      - printmaxx

volumes:
  n8n_data:
    driver: local

networks:
  printmaxx:
    driver: bridge
```

### Launch Commands

```bash
# Create directory
mkdir -p AUTOMATIONS/n8n

# Set password
export N8N_PASSWORD="your-secure-password-here"

# Launch
cd AUTOMATIONS/n8n
docker compose up -d

# Access at http://localhost:5678
# Login: printmaxx / [your password]

# Stop
docker compose down

# View logs
docker compose logs -f n8n

# Update to latest
docker compose pull && docker compose up -d
```

### First-Time Setup

1. Open `http://localhost:5678`
2. Create owner account (printmaxx / your password)
3. Skip the onboarding tutorial
4. Go to Settings > Community Nodes > Enable
5. Install community nodes: `n8n-nodes-mcp` (MCP integration)

---

## Workflow 1: Social Content Posting Queue

**Purpose:** Read approved content from CSV, format per platform, post on schedule.

**Trigger:** Cron schedule (3x daily: 9am, 1pm, 6pm ET)

**Flow:**

```
[Cron Trigger 9am/1pm/6pm]
    |
    v
[Read CSV: AUTOMATIONS/content_posting/posting_queue.csv]
    |
    v
[Filter: status = APPROVED AND scheduled_time <= NOW]
    |
    v
[Switch: platform]
    |
    +--> [Twitter/X] --> [HTTP Request: X API v2] --> [Update CSV: status = POSTED]
    |
    +--> [Reddit] --> [HTTP Request: Reddit API] --> [Update CSV: status = POSTED]
    |
    +--> [LinkedIn] --> [HTTP Request: LinkedIn API] --> [Update CSV: status = POSTED]
    |
    +--> [Beehiiv] --> [HTTP Request: Beehiiv API] --> [Update CSV: status = POSTED]
```

**posting_queue.csv format:**

```csv
post_id,platform,content,scheduled_time,status,niche,content_type,source_alpha,posted_at,post_url
PL001,twitter,"phone locks until you pray. no dismiss button. the lock IS the product.",2026-02-04T09:00:00,APPROVED,faith,social_post,ALPHA478,,
WL003,twitter,"I walked 4 miles yesterday just to check Instagram. down 8 pounds in 6 weeks.",2026-02-04T13:00:00,APPROVED,fitness,social_post,ALPHA479,,
AI005,reddit,"hard paywalls generate 8x more revenue than freemium. here's my data.",2026-02-04T18:00:00,APPROVED,tech,reddit_post,ALPHA465,,
```

**Platform-specific formatting:**
| Platform | Max Length | Formatting | Rate Limit |
|----------|-----------|------------|------------|
| Twitter/X | 280 chars | Plain text, no hashtags (per meta) | 17 tweets/15 min |
| Reddit | 40,000 chars | Markdown, title + body separate | 1 post/10 min |
| LinkedIn | 3,000 chars | Plain text, line breaks for readability | 100 posts/day |
| Beehiiv | Unlimited | HTML, subject + body | API rate limit |

### X/Twitter API Integration

```
Method: POST
URL: https://api.twitter.com/2/tweets
Headers:
  Authorization: Bearer ${X_BEARER_TOKEN}
  Content-Type: application/json
Body:
  { "text": "{{ $json.content }}" }
```

**Required credentials (add to n8n):**
- X API Key + Secret (developer.twitter.com)
- X Access Token + Secret (per account)
- OAuth 2.0 for multi-account posting

### Reddit API Integration

```
Method: POST
URL: https://oauth.reddit.com/api/submit
Headers:
  Authorization: Bearer ${REDDIT_TOKEN}
Body:
  kind: self
  sr: {{ $json.subreddit }}
  title: {{ $json.title }}
  text: {{ $json.content }}
```

**Required:** Reddit app created at reddit.com/prefs/apps (script type).

---

## Workflow 2: Alpha Staging Monitor

**Purpose:** Watch ALPHA_STAGING.csv for new PENDING_REVIEW entries, notify via webhook.

**Trigger:** Every 30 minutes

**Flow:**

```
[Cron: Every 30 min]
    |
    v
[Read CSV: LEDGER/ALPHA_STAGING.csv]
    |
    v
[Filter: status = PENDING_REVIEW AND added_date = TODAY]
    |
    v
[Count items]
    |
    v
[If count > 0]
    |
    v
[Send notification: "X new alpha entries pending review"]
    |
    +--> [Slack/Discord webhook] (if configured)
    +--> [macOS notification via osascript]
    +--> [Email via SMTP]
```

---

## Workflow 3: Revenue Dashboard Daily Digest

**Purpose:** Aggregate daily revenue data across all methods, send morning summary.

**Trigger:** Daily at 8am ET

**Flow:**

```
[Cron: 8am daily]
    |
    v
[Read CSV: FINANCIALS/REVENUE_TRACKER.csv]
    |
    v
[Aggregate: sum by method, sum total, calculate vs yesterday]
    |
    v
[Format: markdown summary]
    |
    v
[Send: email or Slack/Discord]
```

---

## Workflow 4: App Store Review Monitor

**Purpose:** Check for new App Store reviews, flag negative ones.

**Trigger:** Every 6 hours

**Flow:**

```
[Cron: Every 6 hours]
    |
    v
[HTTP Request: App Store Connect API - reviews endpoint]
    |
    v
[Filter: new reviews since last check]
    |
    v
[Switch: rating]
    |
    +--> [1-2 stars] --> [Alert: negative review] --> [Add to response queue]
    +--> [3 stars] --> [Log for analysis]
    +--> [4-5 stars] --> [Extract testimonial for marketing]
```

---

## Workflow 5: Cold Email Sequence Manager

**Purpose:** Manage multi-touch cold email sequences with proper spacing.

**Trigger:** Daily at 10am ET

**Flow:**

```
[Cron: 10am daily]
    |
    v
[Read CSV: MONEY_METHODS/COLD_OUTBOUND/active_sequences.csv]
    |
    v
[Filter: next_touch_date = TODAY]
    |
    v
[For Each prospect]
    |
    v
[Get template for current step (1-5)]
    |
    v
[AI personalization: replace variables with prospect data]
    |
    v
[Send via SMTP (warmed inbox)]
    |
    v
[Update CSV: increment step, set next_touch_date]
    |
    v
[Log to activity tracker]
```

**Deliverability safeguards:**
- Max 50 sends per inbox per day
- Random delay 30-90 seconds between sends
- Skip weekends
- Stop sequence on reply detection
- Rotate sending inboxes

---

## Workflow 6: Content Cascade Trigger

**Purpose:** When a piece of content is marked POSTED on one platform, auto-queue repurposed versions for other platforms.

**Trigger:** Webhook (called when posting_queue.csv status changes to POSTED)

**Flow:**

```
[Webhook: content_posted]
    |
    v
[Read original content]
    |
    v
[Check cascade map: what other platforms need this?]
    |
    v
[For each target platform]
    |
    v
[Reformat content for platform]
    |
    +--> Twitter post --> trim to 280 chars, add hook
    +--> Reddit post --> expand to 500+ words, add data
    +--> LinkedIn --> professional tone adjustment
    +--> Newsletter --> add intro/outro, CTA
    |
    v
[Add to posting_queue.csv with PENDING_REVIEW status]
```

---

## MCP Integration (Future)

n8n supports MCP protocol via community node `n8n-nodes-mcp`. This enables:

1. **Claude as a workflow node** - send content to Claude for rewriting/formatting
2. **Agent-triggered workflows** - Claude Code can trigger n8n workflows via webhook
3. **Database MCP** - n8n reads/writes to any database Claude can access
4. **Tool chaining** - n8n workflow as a tool Claude can call

**Setup:** Install `n8n-nodes-mcp` from community nodes, configure Claude API key.

---

## Credential Management

**Store in n8n's encrypted credential store (NOT in plaintext):**

| Credential | Where to Get | Status |
|------------|-------------|--------|
| X/Twitter API | developer.twitter.com | NEEDS_SETUP |
| Reddit API | reddit.com/prefs/apps | NEEDS_SETUP |
| Beehiiv API | app.beehiiv.com/settings/api | NEEDS_SETUP |
| Gumroad API | gumroad.com/settings/developer | NEEDS_SETUP |
| Stripe API | dashboard.stripe.com/apikeys | NEEDS_SETUP |
| SMTP (cold email) | Email provider | NEEDS_SETUP |
| Claude API | console.anthropic.com | AVAILABLE (in .env) |
| Google Sheets | Google Cloud Console | NEEDS_SETUP |

---

## Implementation Priority

| Workflow | Priority | Dependencies | Build Time |
|----------|----------|-------------|------------|
| 1. Content Posting Queue | HIGHEST | X API + Reddit API | 2 hours |
| 5. Cold Email Sequence | HIGH | SMTP + warmed inboxes | 2 hours |
| 2. Alpha Staging Monitor | MEDIUM | None (CSV only) | 30 min |
| 3. Revenue Dashboard | MEDIUM | FINANCIALS CSVs | 1 hour |
| 6. Content Cascade | LOW (manual first) | Workflow 1 working | 3 hours |
| 4. App Store Reviews | LOW | Apple API key | 1 hour |

**Start with Workflow 1 (content posting) + Workflow 2 (alpha monitor).** These have the highest immediate value and lowest setup friction.

---

## Maintenance

```bash
# Daily health check
docker compose ps

# Backup n8n data
docker compose exec n8n n8n export:workflow --all --output=/home/node/.n8n/backups/

# Update n8n
docker compose pull && docker compose up -d

# Monitor resource usage
docker stats n8n
```

**Resource requirements:** ~200MB RAM idle, spikes to 500MB during workflow execution. Runs fine on any modern Mac.

---

## Human Setup Tasks (Checkpoint)

- [ ] Install Docker Desktop if not already installed
- [ ] Create X/Twitter developer app (developer.twitter.com)
- [ ] Create Reddit app (script type) at reddit.com/prefs/apps
- [ ] Get Beehiiv API key
- [ ] Set up SMTP for cold email sending
- [ ] Run `docker compose up -d` to launch n8n
- [ ] Import workflow JSON files (will be created after Docker setup confirmed)
