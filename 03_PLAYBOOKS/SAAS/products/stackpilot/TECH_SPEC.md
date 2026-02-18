# StackPilot Technical Specification

**Last updated:** 2026-01-20
**Status:** MVP specification

---

## Overview

StackPilot is a prompt library and workflow automation tool. Users save prompts with variables, run them in multiple AI models, and chain them into automated workflows.

Core components:
1. Prompt library (CRUD, folders, tags, search)
2. Variable system ({{placeholders}} with form generation)
3. AI runner (ChatGPT, Claude, Gemini integration)
4. Workflow builder (drag-and-drop, output chaining)
5. Browser extension (save prompts from chat)

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
├─────────────────────────────────────────────────────────────┤
│  Web App         │   Browser Extension  │   Landing Site    │
│  (Next.js)       │   (Chrome/Firefox)   │   (Next.js)       │
└────────┬─────────┴─────────┬────────────┴───────────────────┘
         │                   │
         ▼                   ▼
┌─────────────────────────────────────────────────────────────┐
│                      API Layer                              │
├─────────────────────────────────────────────────────────────┤
│  FastAPI / Python                                           │
│  - /prompts CRUD                                            │
│  - /folders CRUD                                            │
│  - /run execute prompts                                     │
│  - /workflows CRUD + execute                                │
│  - /auth (JWT)                                              │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Service Layer                            │
├─────────────┬────────────────┬──────────────────────────────┤
│   AI        │   Workflow     │   Variable Parser            │
│   Runner    │   Engine       │   (Parse {{vars}},           │
│   (OpenAI,  │   (Sequence    │   generate forms)            │
│   Anthropic,│   execution,   │                              │
│   Google)   │   output       │                              │
│             │   chaining)    │                              │
└─────────────┴────────────────┴──────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer                               │
├─────────────┬────────────────┬──────────────────────────────┤
│   Postgres  │   Redis        │   Blob Storage               │
│   (Users,   │   (Session,    │   (Exported files,           │
│   prompts,  │   rate limits, │   uploaded imports)          │
│   workflows,│   caching)     │                              │
│   folders)  │                │                              │
└─────────────┴────────────────┴──────────────────────────────┘
```

---

## Tech stack

### Backend
- **Runtime:** Python 3.11
- **Framework:** FastAPI
- **AI APIs:** OpenAI (GPT-4), Anthropic (Claude), Google (Gemini)
- **Database:** Supabase Postgres
- **Cache:** Upstash Redis
- **Background jobs:** Celery + Redis (for workflow execution)

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Styling:** Tailwind CSS
- **Components:** Shadcn/ui
- **State:** Zustand
- **Drag-and-drop:** dnd-kit (for workflow builder)
- **Editor:** Monaco (for prompt editing)

### Browser extension
- **Manifest:** V3 (Chrome), V2 fallback (Firefox)
- **Build:** Vite
- **Communication:** Chrome messaging API

### Infrastructure
- **Backend hosting:** Railway
- **Frontend hosting:** Vercel
- **Storage:** Cloudflare R2
- **Monitoring:** Sentry, Posthog

### Cost estimate (0-1000 users)
| Service | Free tier | Paid tier |
|---------|-----------|-----------|
| Railway | $5/month | $20/month |
| Vercel | Free | Free |
| Supabase | Free | $25/month |
| Upstash Redis | Free | $10/month |
| Cloudflare R2 | Free (10GB) | $0.015/GB |
| OpenAI API | ~$50-100/month | Scales |
| Anthropic API | ~$50-100/month | Scales |
| Google AI API | ~$20-50/month | Scales |

**Total MVP cost:** ~$150-400/month

---

## Data models

### User
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255),
  google_id VARCHAR(255),
  github_id VARCHAR(255),
  plan VARCHAR(50) DEFAULT 'free',
  stripe_customer_id VARCHAR(255),
  team_id UUID REFERENCES teams(id),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Team
```sql
CREATE TABLE teams (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  owner_id UUID NOT NULL REFERENCES users(id),
  plan VARCHAR(50) DEFAULT 'team',
  member_limit INTEGER DEFAULT 5,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Prompt
```sql
CREATE TABLE prompts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  team_id UUID REFERENCES teams(id), -- NULL for personal prompts
  folder_id UUID REFERENCES folders(id),
  title VARCHAR(500) NOT NULL,
  description TEXT,
  content TEXT NOT NULL,
  variables JSONB DEFAULT '[]', -- [{name, description, default_value}]
  tags TEXT[] DEFAULT '{}',
  is_public BOOLEAN DEFAULT false,
  run_count INTEGER DEFAULT 0,
  last_run_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_prompts_user ON prompts(user_id);
CREATE INDEX idx_prompts_team ON prompts(team_id);
CREATE INDEX idx_prompts_search ON prompts USING gin(to_tsvector('english', title || ' ' || content));
```

### Folder
```sql
CREATE TABLE folders (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  team_id UUID REFERENCES teams(id),
  name VARCHAR(255) NOT NULL,
  parent_id UUID REFERENCES folders(id),
  color VARCHAR(7), -- hex color
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Workflow
```sql
CREATE TABLE workflows (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  team_id UUID REFERENCES teams(id),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  steps JSONB NOT NULL, -- [{prompt_id, output_variable, input_mapping}]
  run_count INTEGER DEFAULT 0,
  last_run_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### Run history
```sql
CREATE TABLE runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  prompt_id UUID REFERENCES prompts(id),
  workflow_id UUID REFERENCES workflows(id),
  model VARCHAR(50) NOT NULL, -- 'gpt-4', 'claude-sonnet', 'gemini-pro'
  input_variables JSONB,
  output TEXT,
  tokens_used INTEGER,
  duration_ms INTEGER,
  status VARCHAR(20) DEFAULT 'completed', -- 'completed', 'failed', 'cancelled'
  error_message TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_runs_user ON runs(user_id);
CREATE INDEX idx_runs_prompt ON runs(prompt_id);
```

---

## API endpoints

### Authentication
```
POST /auth/register - Create account
POST /auth/login - Get JWT token
POST /auth/google - OAuth with Google
POST /auth/github - OAuth with GitHub
POST /auth/refresh - Refresh token
```

### Prompts
```
GET /prompts - List prompts (with search, filters)
POST /prompts - Create prompt
GET /prompts/:id - Get single prompt
PUT /prompts/:id - Update prompt
DELETE /prompts/:id - Delete prompt
POST /prompts/:id/run - Execute prompt
POST /prompts/:id/duplicate - Duplicate prompt
POST /prompts/import - Import from CSV/text
GET /prompts/export - Export all prompts
```

### Folders
```
GET /folders - List folders (tree structure)
POST /folders - Create folder
PUT /folders/:id - Update folder
DELETE /folders/:id - Delete folder
PUT /prompts/:id/move - Move prompt to folder
```

### Workflows
```
GET /workflows - List workflows
POST /workflows - Create workflow
GET /workflows/:id - Get workflow
PUT /workflows/:id - Update workflow
DELETE /workflows/:id - Delete workflow
POST /workflows/:id/run - Execute workflow
GET /workflows/:id/runs - Get workflow run history
```

### Run
```
POST /run - Execute prompt (generic endpoint)
POST /run/compare - Execute in multiple models
GET /runs - Get run history
GET /runs/:id - Get single run details
```

### Teams
```
POST /teams - Create team
GET /teams/:id - Get team details
POST /teams/:id/invite - Invite member
DELETE /teams/:id/members/:user_id - Remove member
GET /teams/:id/prompts - Get team prompts
```

---

## Variable system

### Variable syntax
```
{{variable_name}}
{{variable_name:default_value}}
{{variable_name|description}}
{{variable_name:default|description}}
```

### Parser logic
```python
import re

def parse_variables(content: str) -> list:
    """Extract variables from prompt content."""
    pattern = r'\{\{([^}]+)\}\}'
    matches = re.findall(pattern, content)

    variables = []
    for match in matches:
        parts = match.split('|')
        name_default = parts[0].split(':')

        variable = {
            'name': name_default[0].strip(),
            'default_value': name_default[1].strip() if len(name_default) > 1 else None,
            'description': parts[1].strip() if len(parts) > 1 else None
        }
        variables.append(variable)

    return variables

def fill_variables(content: str, values: dict) -> str:
    """Replace variables with provided values."""
    for key, value in values.items():
        pattern = rf'\{{\{{{key}(?::[^|}}]*)?(?:\|[^}}]*)?\}}\}}'
        content = re.sub(pattern, value, content)
    return content
```

### Form generation
Frontend generates form fields based on parsed variables:
- Text input for short variables
- Textarea for variables with newlines in default
- Dropdown for variables with pipe-separated options

---

## AI runner

### Supported models
```python
MODELS = {
    'gpt-4': {
        'provider': 'openai',
        'model_id': 'gpt-4',
        'max_tokens': 8192
    },
    'gpt-4o': {
        'provider': 'openai',
        'model_id': 'gpt-4o',
        'max_tokens': 128000
    },
    'claude-sonnet': {
        'provider': 'anthropic',
        'model_id': 'claude-3-sonnet-20240229',
        'max_tokens': 200000
    },
    'claude-haiku': {
        'provider': 'anthropic',
        'model_id': 'claude-3-haiku-20240307',
        'max_tokens': 200000
    },
    'gemini-pro': {
        'provider': 'google',
        'model_id': 'gemini-1.5-pro',
        'max_tokens': 1000000
    }
}
```

### Execution flow
```python
async def run_prompt(prompt_id: str, variables: dict, model: str, user_id: str):
    # 1. Get prompt
    prompt = await get_prompt(prompt_id)

    # 2. Check access
    if not user_can_access(user_id, prompt):
        raise PermissionError()

    # 3. Fill variables
    filled_content = fill_variables(prompt.content, variables)

    # 4. Get model config
    model_config = MODELS[model]

    # 5. Execute
    start_time = time.time()
    result = await call_ai(model_config, filled_content)
    duration = (time.time() - start_time) * 1000

    # 6. Save run history
    await save_run(
        user_id=user_id,
        prompt_id=prompt_id,
        model=model,
        input_variables=variables,
        output=result.text,
        tokens_used=result.tokens,
        duration_ms=duration
    )

    # 7. Update prompt stats
    await update_prompt_stats(prompt_id)

    return result
```

---

## Workflow engine

### Workflow schema
```json
{
  "id": "workflow-123",
  "name": "Blog post generator",
  "steps": [
    {
      "id": "step-1",
      "prompt_id": "prompt-abc",
      "output_variable": "research",
      "model": "claude-sonnet"
    },
    {
      "id": "step-2",
      "prompt_id": "prompt-def",
      "input_mapping": {
        "context": "{{step-1.output}}"
      },
      "output_variable": "outline",
      "model": "gpt-4"
    },
    {
      "id": "step-3",
      "prompt_id": "prompt-ghi",
      "input_mapping": {
        "outline": "{{step-2.output}}",
        "research": "{{step-1.output}}"
      },
      "output_variable": "draft",
      "model": "claude-sonnet"
    }
  ]
}
```

### Execution engine
```python
async def run_workflow(workflow_id: str, initial_variables: dict, user_id: str):
    workflow = await get_workflow(workflow_id)
    context = {**initial_variables}
    results = []

    for step in workflow.steps:
        # Build input variables
        step_variables = {}
        for key, value in step.get('input_mapping', {}).items():
            step_variables[key] = resolve_variable(value, context)

        # Add any initial variables not yet mapped
        for key, value in initial_variables.items():
            if key not in step_variables:
                step_variables[key] = value

        # Execute step
        result = await run_prompt(
            prompt_id=step['prompt_id'],
            variables=step_variables,
            model=step['model'],
            user_id=user_id
        )

        # Store output in context
        context[f"{step['id']}.output"] = result.text
        context[step['output_variable']] = result.text

        results.append({
            'step_id': step['id'],
            'output': result.text,
            'tokens': result.tokens,
            'duration': result.duration_ms
        })

    return {
        'final_output': results[-1]['output'],
        'steps': results
    }
```

---

## Browser extension

### Manifest (Chrome V3)
```json
{
  "manifest_version": 3,
  "name": "StackPilot",
  "version": "1.0.0",
  "description": "Save prompts from any AI chat",
  "permissions": ["activeTab", "storage"],
  "host_permissions": [
    "https://chat.openai.com/*",
    "https://claude.ai/*",
    "https://gemini.google.com/*"
  ],
  "action": {
    "default_popup": "popup.html",
    "default_icon": "icon.png"
  },
  "content_scripts": [
    {
      "matches": ["https://chat.openai.com/*", "https://claude.ai/*"],
      "js": ["content.js"]
    }
  ]
}
```

### Content script features
- Detect prompt text in chat interfaces
- Add "Save to StackPilot" button
- Parse variables automatically from prompt
- Send to API with user token

---

## Security

### Authentication
- JWT tokens (1 hour expiry)
- Refresh tokens (30 days)
- OAuth integration (Google, GitHub)
- Rate limiting per user

### Data protection
- All API traffic over HTTPS
- Passwords hashed with bcrypt
- API keys encrypted at rest
- No plain text storage of sensitive data

### User data
- Prompts and runs belong to user
- Team prompts visible to team members only
- Public prompts indexed for search
- Delete account = delete all data

---

## Development phases

### Phase 1: MVP (3 weeks)
- User auth (email + Google)
- Prompt CRUD
- Basic folders
- Single model execution (Claude)
- Simple search

### Phase 2: Core features (3 weeks)
- Variables system
- Multi-model support
- Run history
- Import/export
- Browser extension

### Phase 3: Workflows (3 weeks)
- Workflow builder UI
- Workflow execution
- Team features
- Shared libraries

### Phase 4: Polish (ongoing)
- Performance optimization
- Additional integrations
- Mobile responsive
- Team analytics

---

## Monitoring

### Metrics to track
- Prompts saved per user
- Prompts run per day
- Workflow completion rate
- Model usage distribution
- Error rates by provider

### Alerts
- API error rate > 1%
- Response time > 10s
- AI provider failures
- Rate limit hits

---

## Cost optimization

### AI costs
- Cache identical prompts (Redis, 1hr TTL)
- Use Haiku for simple prompts
- Rate limit to prevent abuse
- Show token usage to users

### Infrastructure
- Start with free tiers
- Upgrade based on usage
- Use edge functions where possible
- Optimize database queries
