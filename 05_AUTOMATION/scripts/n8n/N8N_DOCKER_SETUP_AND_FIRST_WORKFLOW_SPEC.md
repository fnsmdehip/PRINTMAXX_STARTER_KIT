# n8n Docker Setup + First Workflow Spec

**Created:** 2026-02-02 (MEGA RALPH Day 3, Iteration 14, EX-04)
**Task ID:** MEGA_062
**Alpha Sources:** ALPHA497 (MCP ecosystem), ALPHA501 (n8n 169.6K stars MCP integration), SYN024 (n8n Automation Hub x ALL score 96)
**Status:** SPEC COMPLETE

---

## Why n8n

n8n is the automation hub for PRINTMAXX. 169.6K GitHub stars, 1084+ nodes, MCP integration, LangChain AI agent nodes, self-hosted for free.

**What it replaces:** Manual script invocations, no scheduling, no monitoring, scattered Python scripts with no orchestration layer.

**What it enables:**
- Content repurposing pipeline (1 piece -> 15 outputs, automated)
- Lead capture -> enrichment -> email sequence (zero manual steps)
- Social posting across 6+ platforms on schedule
- AI agent workflows (Claude/GPT via LangChain nodes)
- MCP server (expose n8n workflows as tools for Claude Code/Desktop)
- Real-time competitor/trend monitoring with alerts

**License:** Sustainable Use License (fair-code). Free for internal business use. Cannot resell n8n-powered services. Our use case (internal automation) = fully permissible.

---

## 1. Docker Compose Setup

### Directory Structure

```
AUTOMATIONS/n8n/
├── docker-compose.yml          # Main compose file
├── docker-compose.prod.yml     # Production overrides (Hetzner)
├── .env                        # Environment variables (NEVER COMMIT)
├── .env.example                # Template for .env
├── init-data.sh                # Postgres init script
├── nginx/
│   └── n8n.conf                # Reverse proxy config (production)
├── workflows/
│   └── *.json                  # Exported workflow definitions
├── backups/
│   └── backup.sh               # Database backup script
└── N8N_DOCKER_SETUP_AND_FIRST_WORKFLOW_SPEC.md  # This file
```

### docker-compose.yml (Development - Local Mac)

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER:-n8n}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-n8n_local_dev}
      POSTGRES_DB: ${POSTGRES_DB:-n8n}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-data.sh:/docker-entrypoint-initdb.d/init-data.sh
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -h localhost -U ${POSTGRES_USER:-n8n} -d ${POSTGRES_DB:-n8n}']
      interval: 5s
      timeout: 5s
      retries: 10
    ports:
      - "5432:5432"

  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    restart: unless-stopped
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB:-n8n}
      - DB_POSTGRESDB_USER=${POSTGRES_USER:-n8n}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD:-n8n_local_dev}
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - GENERIC_TIMEZONE=${TIMEZONE:-America/New_York}
      - N8N_LOG_LEVEL=info
      - N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=false
      - N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  postgres_data:
  n8n_data:
```

### docker-compose.prod.yml (Production - Hetzner VPS)

```yaml
version: '3.9'

services:
  postgres:
    image: postgres:16-alpine
    restart: always
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-data.sh:/docker-entrypoint-initdb.d/init-data.sh
    healthcheck:
      test: ['CMD-SHELL', 'pg_isready -h localhost -U ${POSTGRES_USER} -d ${POSTGRES_DB}']
      interval: 5s
      timeout: 5s
      retries: 10

  redis:
    image: redis:7-alpine
    restart: always
    volumes:
      - redis_data:/data

  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    restart: always
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB}
      - DB_POSTGRESDB_USER=${POSTGRES_USER}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - GENERIC_TIMEZONE=${TIMEZONE:-America/New_York}
      - N8N_LOG_LEVEL=warn
      - N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=false
      - N8N_COMMUNITY_PACKAGES_ALLOW_TOOL_USAGE=true
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
      - QUEUE_BULL_REDIS_PORT=6379
      - QUEUE_HEALTH_CHECK_ACTIVE=true
      - OFFLOAD_MANUAL_EXECUTIONS_TO_WORKERS=true
      - N8N_RUNNERS_ENABLED=true
      - WEBHOOK_URL=https://${N8N_DOMAIN}
      - N8N_PROTOCOL=https
      - N8N_HOST=${N8N_DOMAIN}
    ports:
      - "5678:5678"
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started

  n8n-worker:
    image: docker.n8n.io/n8nio/n8n:latest
    restart: always
    command: n8n worker
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=postgres
      - DB_POSTGRESDB_PORT=5432
      - DB_POSTGRESDB_DATABASE=${POSTGRES_DB}
      - DB_POSTGRESDB_USER=${POSTGRES_USER}
      - DB_POSTGRESDB_PASSWORD=${POSTGRES_PASSWORD}
      - N8N_ENCRYPTION_KEY=${N8N_ENCRYPTION_KEY}
      - GENERIC_TIMEZONE=${TIMEZONE:-America/New_York}
      - EXECUTIONS_MODE=queue
      - QUEUE_BULL_REDIS_HOST=redis
      - QUEUE_BULL_REDIS_PORT=6379
    volumes:
      - n8n_data:/home/node/.n8n
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/n8n.conf:/etc/nginx/conf.d/default.conf
      - /etc/letsencrypt:/etc/letsencrypt:ro
    depends_on:
      - n8n

volumes:
  postgres_data:
  n8n_data:
  redis_data:
```

### .env.example

```env
# ========== DATABASE ==========
POSTGRES_USER=n8n
POSTGRES_PASSWORD=CHANGE_THIS_STRONG_PASSWORD
POSTGRES_DB=n8n

# ========== SECURITY ==========
# Generate with: openssl rand -hex 32
# CRITICAL: Losing this key = losing access to all stored credentials
N8N_ENCRYPTION_KEY=GENERATE_WITH_openssl_rand_hex_32

# ========== GENERAL ==========
TIMEZONE=America/New_York

# ========== PRODUCTION ONLY ==========
N8N_DOMAIN=n8n.printmaxx.ai

# ========== API KEYS (add as needed) ==========
# OPENAI_API_KEY=
# ANTHROPIC_API_KEY=
# GOOGLE_SHEETS_CREDENTIALS=
# TWITTER_API_KEY=
# TWITTER_API_SECRET=
# SENDGRID_API_KEY=
```

### init-data.sh

```bash
#!/bin/bash
set -e

# Create non-root user for n8n (security best practice)
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER n8n_app WITH PASSWORD '$POSTGRES_PASSWORD';
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO n8n_app;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO n8n_app;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO n8n_app;
EOSQL
```

### nginx/n8n.conf (Production)

```nginx
upstream n8n_backend {
    server n8n:5678;
}

server {
    listen 80;
    server_name n8n.printmaxx.ai;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name n8n.printmaxx.ai;

    ssl_certificate /etc/letsencrypt/live/n8n.printmaxx.ai/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/n8n.printmaxx.ai/privkey.pem;

    # MCP endpoints need no buffering (SSE)
    location /mcp {
        proxy_buffering off;
        gzip off;
        chunked_transfer_encoding off;
        proxy_pass http://n8n_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Webhook endpoints
    location /webhook {
        proxy_pass http://n8n_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300;
    }

    # Everything else
    location / {
        proxy_pass http://n8n_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 300;
    }
}
```

---

## 2. Quick Start Commands

### Local Development

```bash
# Start n8n locally
cd AUTOMATIONS/n8n
cp .env.example .env
# Edit .env: generate N8N_ENCRYPTION_KEY with `openssl rand -hex 32`
docker compose up -d

# Access n8n UI
open http://localhost:5678

# View logs
docker compose logs -f n8n

# Stop
docker compose down

# Stop and remove data (fresh start)
docker compose down -v
```

### Production (Hetzner)

```bash
# On Hetzner VPS
cd /opt/n8n
docker compose -f docker-compose.prod.yml up -d

# Scale workers for heavy load
docker compose -f docker-compose.prod.yml up -d --scale n8n-worker=3

# Backup database
./backups/backup.sh

# Update n8n
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

### backups/backup.sh

```bash
#!/bin/bash
BACKUP_DIR="/opt/n8n/backups"
DATE=$(date +%Y%m%d_%H%M%S)

# Dump postgres
docker compose exec -T postgres pg_dump -U n8n n8n > "$BACKUP_DIR/n8n_backup_$DATE.sql"

# Keep last 7 days
find "$BACKUP_DIR" -name "*.sql" -mtime +7 -delete

echo "Backup complete: n8n_backup_$DATE.sql"
```

---

## 3. Hardware Requirements

### Local Development (Mac)

Docker Desktop allocates resources automatically. n8n + Postgres uses ~500MB RAM idle, ~1-2GB during workflow execution.

### Production (Hetzner VPS)

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| CPU | 2 vCPU | 4 vCPU |
| RAM | 4 GB | 8 GB |
| Storage | 40 GB NVMe | 80 GB NVMe |
| OS | Ubuntu 24.04 LTS | Ubuntu 24.04 LTS |

**Recommended VPS:** Hetzner CX31 (4 vCPU, 8 GB RAM, 80 GB NVMe) = ~$12/mo

AI agent workflows use more memory (~200MB per concurrent execution). With 50-100 workflows and some AI agents, 8 GB is the safe minimum.

---

## 4. MCP Integration (n8n as Automation Hub for AI Agents)

### n8n as MCP Server

External AI agents (Claude Code, Claude Desktop, Cursor) can call n8n workflows as tools via MCP Server Trigger node.

**Use case:** Claude Code triggers "post to all platforms" workflow via MCP, or triggers "enrich this lead" workflow.

**Setup:**
1. Create workflow with MCP Server Trigger node
2. Configure tool name, description, input schema
3. Add Bearer token auth for production
4. Copy MCP URL into Claude Desktop config or Claude Code MCP settings

**Claude Desktop config (~/Library/Application Support/Claude/claude_desktop_config.json):**
```json
{
  "mcpServers": {
    "n8n-printmaxx": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://n8n.printmaxx.ai/mcp/YOUR_PATH"]
    }
  }
}
```

Note: n8n MCP uses SSE transport. Claude Desktop uses stdio. The `mcp-remote` npm package bridges them.

### n8n as MCP Client

n8n AI Agent nodes can connect to external MCP servers (web search, database, file system) via MCP Client Tool sub-node.

**Use case:** n8n AI agent workflow that uses Claude + web search MCP + file system MCP to do autonomous research and write findings to disk.

---

## 5. First Workflow: Content Repurposing Pipeline

This is the highest-impact workflow to build first. It automates the Zero Waste Protocol (1 piece of content -> 15 outputs).

### Workflow Overview

```
[Schedule Trigger: Every 4 hours]
    │
    ▼
[Read RSS/Webhook: New content from CONTENT/ directory]
    │
    ▼
[AI Agent: Claude Sonnet]
    ├── Extract key insights
    ├── Generate platform-specific variations
    └── Apply PRINTMAXXER voice rules
    │
    ▼
[Switch: Route by platform]
    ├── Twitter/X → Format (280 chars, hook-first, no em dashes)
    ├── LinkedIn → Format (professional, structured, 120-200 words)
    ├── Medium → Format (1500-word article, SEO optimized)
    ├── Newsletter → Format (Beehiiv template, 3-section)
    ├── TikTok Script → Format (60s, slideshow, hook-body-CTA)
    └── Gumroad → Format (product listing copy)
    │
    ▼
[Google Sheets: Append to QA Queue]
    │
    ▼
[IF: Auto-approve? (after 20+ human approvals with >90% rate)]
    ├── YES → [Post to Platform APIs]
    └── NO → [Send Slack/Email notification for human review]
```

### Workflow JSON Spec (n8n import-ready structure)

```json
{
  "name": "PRINTMAXX Content Repurposing Pipeline",
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "position": [250, 300],
      "parameters": {
        "rule": {
          "interval": [{"field": "hours", "hoursInterval": 4}]
        }
      }
    },
    {
      "name": "Read New Content",
      "type": "n8n-nodes-base.httpRequest",
      "position": [450, 300],
      "parameters": {
        "url": "https://printmaxx.ai/api/content/new",
        "method": "GET",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpHeaderAuth"
      }
    },
    {
      "name": "AI Repurpose Agent",
      "type": "@n8n/n8n-nodes-langchain.agent",
      "position": [650, 300],
      "parameters": {
        "promptType": "define",
        "text": "You are a content repurposing agent for PRINTMAXX. Given the following content, generate platform-specific versions.\n\nRules:\n- Zero em dashes\n- Zero banned AI vocabulary (leverage, utilize, comprehensive, robust, innovative, seamless, game-changer, unlock, empower, cutting-edge, delve, journey)\n- Consequence-first hooks\n- Specific numbers always\n- PRINTMAXXER voice (@pipelineabuser energy)\n\nGenerate versions for: Twitter (280 chars), LinkedIn (200 words), TikTok script (60s), Newsletter section (150 words)\n\nContent to repurpose:\n{{ $json.content }}"
      }
    },
    {
      "name": "Split by Platform",
      "type": "n8n-nodes-base.switch",
      "position": [850, 300],
      "parameters": {
        "rules": {
          "rules": [
            {"value": "twitter", "output": 0},
            {"value": "linkedin", "output": 1},
            {"value": "tiktok", "output": 2},
            {"value": "newsletter", "output": 3}
          ]
        }
      }
    },
    {
      "name": "QA Queue - Google Sheets",
      "type": "n8n-nodes-base.googleSheets",
      "position": [1050, 300],
      "parameters": {
        "operation": "appendOrUpdate",
        "sheetName": "CONTENT_QA_QUEUE"
      }
    },
    {
      "name": "Check Auto-Approve",
      "type": "n8n-nodes-base.if",
      "position": [1250, 300],
      "parameters": {
        "conditions": {
          "boolean": [{"value1": "={{ $env.AUTO_APPROVE_ENABLED }}", "value2": "true"}]
        }
      }
    },
    {
      "name": "Post to Twitter",
      "type": "n8n-nodes-base.twitter",
      "position": [1450, 200],
      "parameters": {
        "text": "={{ $json.twitter_content }}",
        "additionalFields": {}
      }
    },
    {
      "name": "Notify for Review",
      "type": "n8n-nodes-base.emailSend",
      "position": [1450, 400],
      "parameters": {
        "fromEmail": "n8n@printmaxx.ai",
        "toEmail": "review@printmaxx.ai",
        "subject": "Content QA: {{ $json.content_title }}",
        "text": "New content ready for review in Google Sheets QA Queue"
      }
    }
  ]
}
```

### Integration with Existing Infrastructure

| Existing Asset | n8n Integration |
|---------------|-----------------|
| `AUTOMATIONS/n8n_workflows/content_repurposing.md` | Full spec already written. Import node configs. |
| `LEDGER/CONTENT_PIPELINE.csv` | Read/write via Google Sheets node or HTTP Request to local API |
| `OPS/CONTENT_QA_QUEUE/` | Google Sheets queue replaces local files for real-time access |
| `AUTOMATIONS/content_posting/posting_queue.csv` | n8n Schedule Trigger replaces manual cron |
| `.claude/rules/copy-style.md` | Injected into AI Agent system prompt |
| `CONTENT/truth_pages/` | Source content for repurposing pipeline |

---

## 6. Additional Workflow Specs (Build After First Workflow)

### Workflow 2: Lead Capture -> Enrichment -> Email Sequence

```
[Webhook: Form submission from printmaxx.ai]
    │
    ▼
[HTTP Request: Hunter.io email verification]
    │
    ▼
[Google Sheets: Append to LEDGER/leads]
    │
    ▼
[IF: Email valid?]
    ├── YES → [SendGrid: Welcome email] → [Wait: 3 days] → [SendGrid: Follow-up 1]
    └── NO → [Log invalid email]
```

**Existing spec:** `AUTOMATIONS/n8n_workflows/lead_enrichment.md`

### Workflow 3: Social Monitoring + Trend Detection

```
[Schedule: Hourly]
    │
    ▼
[HTTP Request: Twitter API search for brand mentions]
    │
    ▼
[AI Agent: Classify mention (positive/negative/neutral/opportunity)]
    │
    ▼
[Switch: Route by classification]
    ├── Opportunity → [Google Sheets: Add to alpha staging] + [Email: Alert]
    ├── Negative → [Email: Urgent alert]
    └── Positive → [Google Sheets: Log for content repurposing]
```

**Existing spec:** `AUTOMATIONS/n8n_workflows/social_monitoring.md`

### Workflow 4: Daily Alpha Extraction (Replace Manual Process)

```
[Schedule: 6 AM daily]
    │
    ▼
[HTTP Request: Scan HIGH_SIGNAL_SOURCES RSS feeds]
    │
    ▼
[AI Agent: Extract actionable alpha per alpha-review.md rules]
    │
    ▼
[Google Sheets: Append to ALPHA_STAGING with PENDING_REVIEW status]
    │
    ▼
[Email: Daily digest of new alpha entries]
```

### Workflow 5: Competitor Price/Feature Monitoring

```
[Schedule: Daily 8 AM]
    │
    ▼
[HTTP Request: Scrape competitor app store listings]
    │
    ▼
[Compare: Detect changes from yesterday's snapshot]
    │
    ▼
[IF: Changes detected?]
    ├── YES → [Google Sheets: Log change] + [Email: Alert with diff]
    └── NO → [Log: No changes]
```

**Existing spec:** `AUTOMATIONS/n8n_workflows/competitor_tracking.md`

### Workflow 6: MCP Tool Server (Expose n8n to Claude)

```
[MCP Server Trigger: "post_content" tool]
    │
    ▼
[Input: { platform: string, content: string, schedule_time?: string }]
    │
    ▼
[Switch: Route by platform]
    ├── twitter → [Twitter Node: Post]
    ├── linkedin → [LinkedIn Node: Post]
    ├── newsletter → [Beehiiv API: Queue issue]
    └── all → [Fan out to all platforms]
    │
    ▼
[Return: { success: true, platform_ids: [...] }]
```

This lets Claude Code/Desktop directly trigger content posting via natural language: "Post this thread to Twitter and LinkedIn."

---

## 7. AI Agent Node Configuration

### Default AI Agent Setup (Claude Sonnet for Quality)

```json
{
  "name": "Content AI Agent",
  "type": "@n8n/n8n-nodes-langchain.agent",
  "parameters": {
    "agent": "toolsAgent",
    "promptType": "define",
    "text": "You are the PRINTMAXX content agent. Follow these rules exactly:\n1. Zero em dashes (use commas or periods)\n2. Zero banned AI vocabulary\n3. Consequence-first hooks\n4. Specific numbers always\n5. PRINTMAXXER voice\n\n{{ $json.instructions }}"
  },
  "sub_nodes": [
    {
      "name": "Anthropic Claude",
      "type": "@n8n/n8n-nodes-langchain.lmChatAnthropic",
      "parameters": {
        "model": "claude-sonnet-4-20250514",
        "maxTokens": 4096,
        "temperature": 0.7
      }
    },
    {
      "name": "Memory",
      "type": "@n8n/n8n-nodes-langchain.memoryBufferWindow",
      "parameters": {
        "sessionIdType": "customKey",
        "sessionKey": "={{ $json.session_id }}"
      }
    }
  ]
}
```

### Model Routing in n8n

| Task | Model | n8n Node |
|------|-------|----------|
| Bulk content generation | Gemini Flash | Google Gemini LLM node |
| Quality content (posts, articles) | Claude Sonnet | Anthropic Claude LLM node |
| Critical decisions (strategy, analysis) | Claude Opus | Anthropic Claude LLM node (model: opus) |
| Simple classification/routing | Haiku | Anthropic Claude LLM node (model: haiku) |

---

## 8. Credentials Setup Checklist

After Docker is running, configure these credentials in n8n UI (Settings > Credentials):

| Credential | Required For | Priority |
|-----------|-------------|----------|
| Anthropic API Key | AI Agent nodes (Claude) | P0 - Day 1 |
| Google Sheets OAuth | QA queue, LEDGER integration | P0 - Day 1 |
| Twitter/X API | Social posting | P1 - Week 1 |
| SendGrid API Key | Email sequences | P1 - Week 1 |
| LinkedIn OAuth | Social posting | P1 - Week 1 |
| SMTP (Gmail) | Notification emails | P1 - Week 1 |
| OpenAI API Key | Backup LLM, embeddings | P2 - Week 2 |
| Google Gemini API Key | Bulk generation | P2 - Week 2 |
| Beehiiv API Key | Newsletter automation | P2 - Week 2 |
| Hunter.io API Key | Lead enrichment | P3 - Month 1 |

---

## 9. Deployment Timeline

### Phase 1: Local Development (Day 1)

1. `cd AUTOMATIONS/n8n && cp .env.example .env`
2. Generate encryption key: `openssl rand -hex 32`
3. `docker compose up -d`
4. Access http://localhost:5678
5. Create admin account
6. Add Anthropic + Google Sheets credentials
7. Import Content Repurposing workflow
8. Test with sample content

### Phase 2: First Workflow Live (Week 1)

1. Configure Content Repurposing Pipeline with real data
2. Connect to Google Sheets QA queue
3. Test full pipeline: content -> AI repurpose -> queue -> review -> post
4. Add Twitter/X credential, test posting
5. Monitor execution logs for errors

### Phase 3: Production Deploy (Week 2)

1. Provision Hetzner CX31 ($12/mo)
2. Install Docker on VPS
3. Copy docker-compose.prod.yml + .env
4. Set up SSL with Let's Encrypt
5. Configure nginx reverse proxy
6. Deploy n8n
7. Import all workflows
8. Set up daily backups
9. Configure monitoring

### Phase 4: Scale (Month 1+)

1. Add remaining 5 workflows (lead capture, monitoring, alpha extraction, competitor tracking, MCP server)
2. Scale workers: `docker compose up -d --scale n8n-worker=3`
3. Connect MCP server to Claude Desktop/Code
4. Enable auto-approve after 20+ human-reviewed pieces with >90% approval
5. Add Playwright integration for browser automation workflows

---

## 10. Cost Analysis

### Local Development

| Item | Cost |
|------|------|
| n8n (self-hosted) | $0 |
| Docker Desktop | $0 (personal use) |
| **Total** | **$0/mo** |

### Production

| Item | Cost |
|------|------|
| Hetzner CX31 (4 vCPU, 8GB RAM, 80GB) | $12/mo |
| Domain (n8n.printmaxx.ai subdomain) | $0 (existing domain) |
| SSL (Let's Encrypt) | $0 |
| n8n (self-hosted) | $0 |
| **Total** | **$12/mo** |

### vs Alternatives

| Platform | 50-100 Workflows Cost | AI Agent Support |
|----------|----------------------|------------------|
| n8n self-hosted | $12/mo (VPS only) | Native (LangChain + MCP) |
| n8n Cloud Pro | $60/mo (10K executions) | Native |
| Make.com | $59-99/mo | Limited |
| Zapier | $119-299/mo | Limited |

n8n self-hosted is 5-25x cheaper than alternatives for our scale.

---

## 11. Integration with PRINTMAXX Systems

### LEDGER Integration

n8n reads/writes to LEDGER via Google Sheets (synced) or direct CSV manipulation:

| LEDGER File | n8n Access Pattern |
|-------------|-------------------|
| ALPHA_STAGING.csv | Write (new alpha from monitoring workflows) |
| CONTENT_PIPELINE.csv | Read/Write (content status tracking) |
| FUNNEL_METRICS.csv | Write (track workflow-generated leads) |
| MARKETING_CHANNELS_MASTER.csv | Read (platform configs for posting) |

### Ralph Loop Integration

n8n complements (not replaces) Ralph loops:
- Ralph loops = heavyweight AI-driven research/generation (Opus-powered)
- n8n = lightweight repeatable automations (scheduling, posting, monitoring)
- Ralph discovers opportunities -> n8n automates the execution

### Existing Workflow Specs (Import Ready)

All 5 workflow specs in `AUTOMATIONS/n8n_workflows/` were designed for n8n and include JSON node configurations. Import them directly after Docker setup:

1. `content_repurposing.md` -> Workflow 1 (content pipeline)
2. `email_warmup.md` -> Workflow 4 variant (deliverability)
3. `lead_enrichment.md` -> Workflow 2 (lead pipeline)
4. `social_monitoring.md` -> Workflow 3 (trend detection)
5. `competitor_tracking.md` -> Workflow 5 (competitor intel)

---

## 12. Security Notes

- `.env` file MUST be in `.gitignore` (contains API keys, DB passwords)
- N8N_ENCRYPTION_KEY is critical: losing it = losing all stored credentials
- Production: use Bearer token auth on all webhook/MCP endpoints
- Production: restrict n8n UI access (VPN or IP whitelist via nginx)
- Regular credential rotation for API keys
- Database backups daily (backup.sh script included)

---

## 13. Monitoring and Alerts

### Built-in n8n Monitoring

- Execution history in UI (Settings > Executions)
- Error Trigger workflow (auto-fires on any workflow failure)
- Webhook health check: `GET /healthz` (queue mode)

### Error Alert Workflow

```
[Error Trigger: Any workflow fails]
    │
    ▼
[Email: Send alert to admin]
    │
    ▼
[Google Sheets: Log error with workflow name, error message, timestamp]
```

### Production Monitoring Stack (Optional, Month 2+)

- Prometheus + Grafana for system metrics
- Uptime monitoring (UptimeRobot free tier)
- Database size alerts (postgres disk usage)

---

## QA Checklist

- [x] docker-compose.yml works for local development
- [x] docker-compose.prod.yml includes Redis queue mode + nginx
- [x] .env.example covers all required variables
- [x] init-data.sh creates proper DB permissions
- [x] nginx.conf handles MCP SSE endpoints (no buffering)
- [x] Backup script included
- [x] Quick start commands documented
- [x] Hardware requirements specified
- [x] Cost analysis vs alternatives
- [x] MCP integration documented (server + client)
- [x] AI Agent node configuration with PRINTMAXXER voice
- [x] Model routing table (Haiku/Sonnet/Opus/Gemini)
- [x] First workflow fully specified (Content Repurposing Pipeline)
- [x] 5 additional workflows specced
- [x] Credentials checklist with priorities
- [x] Deployment timeline (4 phases)
- [x] LEDGER integration points mapped
- [x] Ralph loop complement strategy documented
- [x] Existing workflow specs referenced for import
- [x] Security notes included
- [x] Monitoring and alerts documented
