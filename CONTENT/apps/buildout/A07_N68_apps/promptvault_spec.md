# PromptVault — Feature Spec

**Concept:** A personal + marketplace platform for AI prompt management. Save, organize, and sell prompts. Think Notion meets Gumroad but for AI prompts.

**Target User:** AI power users, content creators, developers, solopreneurs who use Claude/GPT/Midjourney daily and want to monetize their best prompts.

**Category:** Productivity / AI Tools
**Platform:** Web app (Next.js) + Chrome Extension
**Pricing:**
- Free: up to 50 personal prompts
- Pro ($9/mo): unlimited prompts, folders, team sharing, analytics
- Marketplace: 20% platform fee on prompt sales (seller keeps 80%)

**Revenue Target:** $3,000/mo — 200 Pro subs ($1,800) + $6,000 GMV marketplace ($1,200 fees)

---

## Core Differentiator

PromptBase charges 20% + sells at fixed prices. PromptVault:
1. Better organization (folders, tags, search, versioning)
2. Seller keeps more (80% vs 60-70% on competitors)
3. Prompt testing built in (run prompt directly from vault against GPT-4o or Claude)
4. Team/agency vaults (share prompts with your team, track usage)
5. Chrome extension: inject any saved prompt into any AI chat in 2 clicks

---

## MVP Features (v1.0)

### 1. Personal Vault
- Save prompts with: title, body, model tag (GPT-4o/Claude/Gemini/Midjourney/DALL-E/Sora), category, tags
- Folders: unlimited nesting (Pro) / 5 folders (Free)
- Search: full-text search across all prompts
- Variables: `{{placeholder}}` syntax — fill in variables at run time
  - Example: "Write a cold email for {{company}} targeting {{pain_point}} in under 100 words"
  - At run time: fills in variables before copying/sending
- Version history: see all edits, revert to any version (Pro)
- Prompt notes: private notes on what the prompt is good for
- Favorites / pin prompts

### 2. Prompt Runner (Built-in Testing)
- Run prompt directly in PromptVault against:
  - OpenAI API (GPT-4o, GPT-4o-mini, o1) — user provides own API key
  - Anthropic API (Claude 3.5 Sonnet, Haiku) — user provides own API key
- See output, rate it (thumbs up/down), add notes
- Compare: run same prompt against 2 models side by side
- Cost estimate shown per run (token count × price)
- Version comparison: run v1 vs v2 of same prompt, see outputs side by side

### 3. Chrome Extension
- Keyboard shortcut: `Ctrl+Shift+P` opens prompt picker overlay on any page
- Works on: ChatGPT, Claude.ai, Gemini, Perplexity, any `<textarea>`
- Search prompts, click to inject (fills the input field)
- Variable substitution happens in the extension popup before injecting
- Recent prompts: last 5 used shown immediately (no search needed)
- Sync: extension syncs with web vault in real time

### 4. Marketplace
- Public listing: set prompt as public with a price ($0.99-$99)
- Listing fields: title, description, sample output, model, category, tags, price
- Preview: buyer sees first 30% of prompt, blurred after
- Purchase flow: Stripe → instant unlock → saved to buyer's vault
- Ratings: 5-star after purchase
- Seller dashboard: sales count, revenue, conversion rate, views
- Featured listings: curated by PromptVault team (no pay-to-play in v1)

### 5. Team Vaults (Pro+)
- Invite team members via email
- Shared vault folder (all can edit)
- Usage tracking: see who used which prompt, when
- Admin controls: lock prompts (read-only for team), archive
- Billing: 1 Pro seat covers team of 5 (Pro plan)

---

## Technical Architecture

### Stack
```
Frontend:  Next.js 14 (App Router) + TypeScript + Tailwind + shadcn/ui
Backend:   Supabase (Postgres + Auth + Storage + Realtime)
Payments:  Stripe (subscriptions + marketplace payouts)
Extension: Chrome MV3 (Manifest v3) + React
Search:    Postgres full-text search (upgrade to Typesense at scale)
AI Runner: OpenAI SDK + Anthropic SDK (user-supplied keys, never stored server-side)
Deploy:    Vercel (Next.js) + Supabase cloud
```

### Database Schema (simplified)
```sql
-- Prompts
CREATE TABLE prompts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  model TEXT,  -- gpt-4o, claude-3-5-sonnet, etc.
  category TEXT,
  tags TEXT[],
  folder_id UUID REFERENCES folders(id),
  is_public BOOLEAN DEFAULT false,
  price DECIMAL(10,2),  -- null = free public, 0 = free, >0 = paid
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- Prompt versions
CREATE TABLE prompt_versions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  prompt_id UUID REFERENCES prompts(id) NOT NULL,
  body TEXT NOT NULL,
  version_number INTEGER NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Marketplace purchases
CREATE TABLE purchases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  prompt_id UUID REFERENCES prompts(id) NOT NULL,
  buyer_id UUID REFERENCES auth.users NOT NULL,
  seller_id UUID REFERENCES auth.users NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  stripe_payment_intent TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Ratings
CREATE TABLE ratings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  prompt_id UUID REFERENCES prompts(id) NOT NULL,
  user_id UUID REFERENCES auth.users NOT NULL,
  score INTEGER CHECK (score BETWEEN 1 AND 5),
  review TEXT,
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(prompt_id, user_id)
);
```

### Chrome Extension Architecture (Manifest v3)
```json
{
  "manifest_version": 3,
  "name": "PromptVault",
  "version": "1.0.0",
  "permissions": ["storage", "activeTab", "scripting"],
  "host_permissions": ["https://chat.openai.com/*", "https://claude.ai/*", "https://gemini.google.com/*"],
  "background": { "service_worker": "background.js" },
  "action": { "default_popup": "popup.html" },
  "commands": {
    "_execute_action": { "suggested_key": { "default": "Ctrl+Shift+P" } }
  }
}
```

Content script injection:
```javascript
// Detect target AI platform
const PLATFORMS = {
  'chat.openai.com': '#prompt-textarea',
  'claude.ai': '[data-testid="chat-input"]',
  'gemini.google.com': '.input-area-container textarea'
};

function injectPrompt(promptText) {
  const selector = PLATFORMS[window.location.hostname];
  if (!selector) return;
  const el = document.querySelector(selector);
  if (!el) return;
  const nativeInputValueSetter = Object.getOwnPropertyDescriptor(
    window.HTMLTextAreaElement.prototype, 'value'
  ).set;
  nativeInputValueSetter.call(el, promptText);
  el.dispatchEvent(new Event('input', { bubbles: true }));
}
```

---

## Monetization Detail

### Pro Subscription ($9/mo or $79/yr)
| Feature | Free | Pro |
|---|---|---|
| Personal prompts | 50 | Unlimited |
| Folders | 5 | Unlimited |
| Version history | None | Full |
| Team vault | No | Up to 5 members |
| Bulk export | No | JSON/CSV |
| Analytics | None | Usage tracking |
| Priority support | No | Yes |
| Prompt runner | 10 runs/day | Unlimited |

### Marketplace Economics
- Seller lists prompt at any price ($0.99-$99)
- PromptVault takes 20% (vs PromptBase's 40%)
- Instant Stripe payout (vs PromptBase's manual weekly)
- At $6,000 GMV: PromptVault earns $1,200 in fees
- Scale target: $30,000 GMV by month 12 = $6,000/mo fees

### Revenue Model at Scale
| Revenue Stream | Month 6 | Month 12 |
|---|---|---|
| Pro subscriptions | $2,700 (300 users) | $7,200 (800 users) |
| Marketplace fees (20%) | $800 | $3,000 |
| Team plans (Pro × seats) | $450 | $1,500 |
| **Total** | **$3,950** | **$11,700** |

---

## App Store / Distribution

**Product Hunt launch:**
- Post: "PromptVault — save, organize, and sell your best AI prompts"
- Hunter: reach out to active PH hunters 2 weeks before
- Launch day: post in r/ChatGPT, r/ClaudeAI, r/artificial

**SEO targets:**
- "prompt manager" — 2,400/mo, KD 28
- "chatgpt prompt library" — 8,100/mo, KD 32
- "best prompts for claude" — 1,600/mo, KD 22
- "sell ai prompts" — 1,900/mo, KD 30

**Chrome Web Store listing:**
Title: PromptVault — AI Prompt Manager
Short description: Save, organize, and inject prompts into ChatGPT, Claude, and Gemini in 2 clicks.
Category: Productivity

---

## Competitive Analysis

| Platform | Seller Cut | Organization | Testing | Extension |
|---|---|---|---|---|
| PromptBase | 60-70% | Basic tags | No | No |
| FlowGPT | 60% | Folders | Limited | No |
| Promptrr | 70% | Basic | No | No |
| **PromptVault** | **80%** | **Folders + tags + versions** | **Built-in runner** | **Yes** |

---

## Build Timeline

| Phase | Duration | Deliverable |
|---|---|---|
| Core vault + auth | Week 1-2 | Save/search/folder prompts |
| Chrome extension | Week 3 | Inject into ChatGPT/Claude |
| Marketplace | Week 4-5 | List + purchase + Stripe |
| Pro subscription | Week 5 | Stripe billing |
| Prompt runner | Week 6 | API key integration |
| Launch | Week 7 | Product Hunt |

**Stack costs:**
- Supabase: $0 (free tier) → $25/mo at scale
- Vercel: $0 (hobby) → $20/mo Pro
- Stripe: 2.9% + $0.30 per transaction
- Break-even: ~15 Pro subs ($135/mo) covers hosting
