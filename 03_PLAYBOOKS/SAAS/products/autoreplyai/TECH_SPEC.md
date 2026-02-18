# AutoReplyAI Technical Specification

**Last updated:** 2026-01-20
**Status:** MVP specification

---

## Overview

AutoReplyAI is an AI-powered customer service chatbot. It reads customer knowledge bases and answers questions using RAG (Retrieval Augmented Generation).

Core components:
1. Knowledge base ingestion and vectorization
2. Chat widget (embeddable)
3. Integration layer (Slack, email, Shopify)
4. Admin dashboard
5. AI response engine

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
├─────────────────────────────────────────────────────────────┤
│  Chat Widget    │   Admin Dashboard   │   Landing Site      │
│  (React embed)  │   (Next.js)         │   (Next.js)         │
└────────┬────────┴─────────┬───────────┴─────────────────────┘
         │                  │
         ▼                  ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Layer                              │
├─────────────────────────────────────────────────────────────┤
│  FastAPI / Python                                           │
│  - /chat endpoint (websocket)                               │
│  - /knowledge CRUD                                          │
│  - /conversations query                                     │
│  - /integrations config                                     │
│  - /auth (JWT)                                              │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Service Layer                            │
├─────────────┬────────────────┬──────────────────────────────┤
│   RAG       │   Integrations │   Conversation Manager       │
│   Engine    │   (Slack,      │   (History, handoff,         │
│   (LangChain│   Email,       │   analytics)                 │
│   + Pinecone│   Shopify)     │                              │
│   + Claude) │                │                              │
└─────────────┴────────────────┴──────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                               │
├─────────────┬────────────────┬──────────────────────────────┤
│   Postgres  │   Pinecone     │   Redis                      │
│   (Users,   │   (Vector      │   (Session cache,            │
│   convos,   │   embeddings)  │   rate limiting)             │
│   settings) │                │                              │
└─────────────┴────────────────┴──────────────────────────────┘
```

---

## Tech stack

### Backend
- **Runtime:** Python 3.11
- **Framework:** FastAPI
- **AI/ML:** LangChain, Claude API (claude-3-haiku for speed, sonnet for quality)
- **Vector DB:** Pinecone (free tier: 100k vectors)
- **Database:** Supabase Postgres (free tier: 500MB)
- **Cache:** Upstash Redis (free tier: 10k requests/day)
- **Background jobs:** Celery + Redis

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS
- **Components:** Shadcn/ui
- **State:** Zustand
- **Forms:** React Hook Form + Zod

### Widget
- **Build:** Vite (produces single JS file)
- **Size target:** < 50KB gzipped
- **Styling:** CSS-in-JS (no external stylesheets)

### Infrastructure
- **Hosting:** Railway (backend) or Render
- **Frontend hosting:** Vercel
- **Widget CDN:** Cloudflare
- **File storage:** Cloudflare R2 (S3-compatible, cheap)
- **Monitoring:** Sentry (errors), Posthog (analytics)

### Cost estimate (0-1000 users)
| Service | Free tier | Paid tier (if needed) |
|---------|-----------|----------------------|
| Railway | $5/month | $20/month |
| Vercel | Free | Free |
| Supabase | Free | $25/month |
| Pinecone | Free (100k vectors) | $70/month |
| Upstash Redis | Free | $10/month |
| Cloudflare R2 | Free (10GB) | $0.015/GB |
| Claude API | ~$50-200/month | Scales with usage |

**Total MVP cost:** ~$100-300/month

---

## Data models

### User
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  company_name VARCHAR(255),
  plan VARCHAR(50) DEFAULT 'free',
  stripe_customer_id VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Knowledge base
```sql
CREATE TABLE knowledge_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(500),
  content TEXT NOT NULL,
  source_type VARCHAR(50), -- 'manual', 'url', 'upload'
  source_url VARCHAR(1000),
  pinecone_ids TEXT[], -- Array of vector IDs
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Conversation
```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  visitor_id VARCHAR(255), -- Anonymous visitor tracking
  channel VARCHAR(50), -- 'widget', 'slack', 'email'
  status VARCHAR(50) DEFAULT 'active', -- 'active', 'resolved', 'handed_off'
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Message
```sql
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
  role VARCHAR(20) NOT NULL, -- 'user', 'assistant', 'human_agent'
  content TEXT NOT NULL,
  confidence FLOAT, -- AI confidence score (0-1)
  sources TEXT[], -- Knowledge base item IDs used
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Integration config
```sql
CREATE TABLE integrations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  type VARCHAR(50) NOT NULL, -- 'slack', 'email', 'shopify'
  config JSONB NOT NULL, -- Encrypted tokens, settings
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

---

## API endpoints

### Authentication
```
POST /auth/register - Create account
POST /auth/login - Get JWT token
POST /auth/refresh - Refresh token
POST /auth/password-reset - Request password reset
```

### Knowledge base
```
GET /knowledge - List all knowledge items
POST /knowledge - Add new item (text, URL, or file)
GET /knowledge/:id - Get single item
PUT /knowledge/:id - Update item
DELETE /knowledge/:id - Delete item
POST /knowledge/crawl - Crawl URL for content
POST /knowledge/upload - Upload file
```

### Chat (public, for widget)
```
WS /chat/:widget_id - WebSocket connection for chat
POST /chat/:widget_id/message - HTTP fallback for message
GET /chat/:widget_id/history - Get conversation history (with visitor token)
```

### Conversations (dashboard)
```
GET /conversations - List conversations (paginated)
GET /conversations/:id - Get conversation with messages
PUT /conversations/:id/status - Update status (resolve, hand off)
POST /conversations/:id/message - Send human response
```

### Settings
```
GET /settings/widget - Get widget configuration
PUT /settings/widget - Update widget config (colors, greeting, etc.)
GET /settings/ai - Get AI settings
PUT /settings/ai - Update AI settings (confidence threshold, tone)
```

### Integrations
```
GET /integrations - List all integrations
POST /integrations/slack/connect - OAuth flow for Slack
POST /integrations/email/setup - Configure email forwarding
POST /integrations/shopify/install - Shopify app install
DELETE /integrations/:id - Remove integration
```

### Analytics
```
GET /analytics/overview - Summary stats
GET /analytics/conversations - Conversation volume over time
GET /analytics/resolution - Resolution rates
GET /analytics/topics - Common question topics
```

---

## RAG pipeline

### Ingestion flow
1. User adds content (paste text, upload file, or provide URL)
2. Content extracted and cleaned
3. Text chunked (500 tokens, 50 token overlap)
4. Each chunk embedded using OpenAI text-embedding-3-small
5. Vectors stored in Pinecone with metadata (source, user_id)
6. Source content stored in Postgres

### Query flow
1. User message received via WebSocket
2. Message embedded using same model
3. Query Pinecone for top 5 similar chunks (filtered by user_id)
4. Chunks assembled into context
5. Prompt sent to Claude:
   - System: "You are a helpful customer service agent. Use only the provided context to answer. If unsure, say so."
   - Context: [Retrieved chunks]
   - User message
6. Response streamed back via WebSocket
7. Confidence calculated from response and source relevance
8. Conversation stored in Postgres

### Confidence scoring
```python
def calculate_confidence(response, sources):
    # Factors:
    # - Relevance of retrieved chunks (Pinecone scores)
    # - Response certainty signals ("I'm not sure", "I don't have info")
    # - Source coverage (did we find relevant docs?)

    avg_source_score = mean([s.score for s in sources])
    uncertainty_signals = count_uncertainty_phrases(response)

    confidence = avg_source_score * (1 - 0.2 * uncertainty_signals)
    return max(0, min(1, confidence))
```

---

## Widget specification

### Embed code
```html
<script>
  window.AutoReplyAI = {
    widgetId: 'abc123',
    position: 'bottom-right'
  };
</script>
<script src="https://cdn.autoreplyai.io/widget.js" async></script>
```

### Widget features
- Chat interface (conversation history persisted in localStorage)
- Typing indicators
- Read receipts
- File upload (images only, < 5MB)
- Minimize/maximize
- Mobile responsive
- Customizable colors via dashboard
- Customizable greeting message
- Customizable launcher icon

### Technical requirements
- < 50KB gzipped
- Load time < 500ms
- Works in all modern browsers (Chrome, Firefox, Safari, Edge)
- No external dependencies
- Shadow DOM for style isolation
- Cross-origin compatible

---

## Integration specifications

### Slack integration
- OAuth 2.0 flow for workspace connection
- Bot listens in specified channels
- Responds in thread under user message
- Commands: `/autoreply-status`, `/autoreply-handoff`
- Events API for message handling

### Email integration
- Unique forwarding address per user
- Parse incoming emails (sender, subject, body)
- Draft response and wait for approval (default)
- Auto-send option for high-confidence
- Reply in same thread

### Shopify integration
- App store listing
- OAuth for store connection
- Inject widget code automatically
- Access order data for tracking questions
- Pre-trained on e-commerce FAQ

---

## Security

### Data handling
- All data encrypted at rest (Supabase default)
- All traffic over HTTPS
- JWT tokens expire in 1 hour (refresh tokens: 30 days)
- Password hashing with bcrypt (cost factor 12)
- Rate limiting: 100 requests/minute per IP

### Compliance
- GDPR: Data export and deletion available
- SOC 2 Type II: In progress (target Q3 2026)
- No PII used for model training
- Data retention: 90 days default, configurable

### API security
- All endpoints require authentication except:
  - Widget chat endpoints (use widget ID + visitor token)
  - Public landing pages
- CORS configured per-user for widget domains

---

## Development phases

### Phase 1: MVP (4 weeks)
- User auth and dashboard
- Knowledge base CRUD
- Basic chat widget
- Claude integration with RAG
- Conversation history

### Phase 2: Integrations (4 weeks)
- Slack integration
- Email integration
- Shopify app

### Phase 3: Scale (4 weeks)
- Analytics dashboard
- Confidence tuning UI
- Human handoff workflow
- Team members (multiple seats)
- Billing (Stripe)

### Phase 4: Polish (ongoing)
- Performance optimization
- Mobile apps
- More integrations
- Enterprise features

---

## Monitoring and observability

### Error tracking
- Sentry for Python and JavaScript errors
- Alert on error spike (> 5/minute)

### Performance
- Response time tracking (target: < 3s for AI response)
- Widget load time (target: < 500ms)
- API latency percentiles (p50, p95, p99)

### Business metrics
- Conversations per day
- Automation rate (AI-only vs human-assisted)
- Customer satisfaction (if ratings enabled)
- Churn indicators

### Alerts
- API errors > 1% of requests
- Response time > 10s
- Pinecone query failures
- Claude API rate limits

---

## Cost optimization

### AI costs
- Use Haiku for most responses ($0.00025/1k tokens)
- Escalate to Sonnet for low-confidence only ($0.003/1k tokens)
- Cache common questions (Redis)
- Batch embeddings where possible

### Infrastructure
- Start with free tiers everywhere
- Upgrade only when limits hit
- Use Cloudflare for CDN (free tier generous)
- Avoid over-provisioning

### Database
- Index frequently queried columns
- Archive old conversations (> 90 days)
- Use connection pooling
