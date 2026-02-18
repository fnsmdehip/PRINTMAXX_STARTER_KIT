# PromptVault - Technical Specification

---

## Stack Overview

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Web Framework | Next.js 14 | SEO, SSR, App Router |
| Mobile | React Native | Cross-platform mobile |
| Backend | Supabase | Auth, DB, real-time, free tier |
| AI | OpenAI API | GPT-4o-mini for cost efficiency |
| Payments (Web) | Stripe | Industry standard |
| Payments (Mobile) | RevenueCat | Mobile subscriptions |
| Search | Fuse.js | Client-side fuzzy search |
| Analytics | Mixpanel | Free tier sufficient |
| Hosting | Vercel | Free tier, Next.js optimized |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       PromptVault                            │
├─────────────────────────────────────────────────────────────┤
│  Clients                                                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐         │
│  │   Web App    │ │   iOS App    │ │ Android App  │         │
│  │  (Next.js)   │ │(React Native)│ │(React Native)│         │
│  └──────────────┘ └──────────────┘ └──────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  API Layer (Next.js API Routes)                              │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐              │
│  │ /prompts   │ │ /improve   │ │ /generate  │              │
│  └────────────┘ └────────────┘ └────────────┘              │
├─────────────────────────────────────────────────────────────┤
│  Services                                                    │
│  ┌────────────┐ ┌────────────┐ ┌────────────┐              │
│  │  Supabase  │ │  OpenAI    │ │  Stripe    │              │
│  │  (Auth/DB) │ │  (AI API)  │ │ (Payments) │              │
│  └────────────┘ └────────────┘ └────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

---

## Web App (Next.js)

### File Structure

```
promptvault-web/
├── app/
│   ├── (marketing)/
│   │   ├── page.tsx              # Landing page
│   │   └── pricing/page.tsx      # Pricing page
│   ├── (app)/
│   │   ├── layout.tsx            # App layout with sidebar
│   │   ├── prompts/
│   │   │   ├── page.tsx          # Prompt library
│   │   │   └── [category]/page.tsx
│   │   ├── improve/page.tsx      # Prompt improver (Pro)
│   │   ├── generate/page.tsx     # Prompt generator (Pro)
│   │   ├── favorites/page.tsx    # User favorites
│   │   ├── history/page.tsx      # Prompt history (Pro)
│   │   └── settings/page.tsx
│   ├── api/
│   │   ├── prompts/route.ts
│   │   ├── improve/route.ts
│   │   ├── generate/route.ts
│   │   └── webhooks/stripe/route.ts
│   ├── layout.tsx
│   └── globals.css
├── components/
│   ├── PromptCard.tsx
│   ├── PromptModal.tsx
│   ├── SearchBar.tsx
│   ├── CategoryFilter.tsx
│   ├── Paywall.tsx
│   └── ui/                       # shadcn components
├── lib/
│   ├── supabase.ts
│   ├── openai.ts
│   ├── stripe.ts
│   └── prompts.ts
├── data/
│   └── prompts.json              # Prompt library
└── package.json
```

---

## Database Schema (Supabase)

### Tables

```sql
-- Users table (extends Supabase auth)
create table public.profiles (
  id uuid references auth.users primary key,
  email text,
  is_pro boolean default false,
  stripe_customer_id text,
  subscription_status text,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- User favorites
create table public.favorites (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references public.profiles(id),
  prompt_id text not null,
  created_at timestamp with time zone default now(),
  unique(user_id, prompt_id)
);

-- User-created prompts (Pro feature)
create table public.user_prompts (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references public.profiles(id),
  title text not null,
  content text not null,
  category text,
  tags text[],
  folder_id uuid,
  created_at timestamp with time zone default now(),
  updated_at timestamp with time zone default now()
);

-- Folders (Pro feature)
create table public.folders (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references public.profiles(id),
  name text not null,
  parent_id uuid references public.folders(id),
  created_at timestamp with time zone default now()
);

-- Prompt history (Pro feature)
create table public.prompt_history (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references public.profiles(id),
  type text not null, -- 'improve' or 'generate'
  input text not null,
  output text not null,
  created_at timestamp with time zone default now()
);

-- Usage tracking
create table public.usage (
  id uuid primary key default uuid_generate_v4(),
  user_id uuid references public.profiles(id),
  action text not null, -- 'improve', 'generate', 'copy'
  prompt_id text,
  created_at timestamp with time zone default now()
);
```

### Row Level Security

```sql
-- Enable RLS
alter table public.profiles enable row level security;
alter table public.favorites enable row level security;
alter table public.user_prompts enable row level security;
alter table public.folders enable row level security;
alter table public.prompt_history enable row level security;

-- Users can only access their own data
create policy "Users can view own profile"
  on public.profiles for select
  using (auth.uid() = id);

create policy "Users can update own profile"
  on public.profiles for update
  using (auth.uid() = id);

-- Similar policies for other tables...
```

---

## Prompt Library Data Structure

```typescript
// data/prompts.json
interface Prompt {
  id: string;
  title: string;
  content: string;
  category: Category;
  tags: string[];
  preview: string;      // First 100 chars
  useCases: string[];   // Example use cases
  tips: string;         // Usage tips
  createdAt: string;
  updatedAt: string;
}

type Category =
  | 'writing'
  | 'coding'
  | 'marketing'
  | 'analysis'
  | 'creative'
  | 'business'
  | 'productivity'
  | 'learning'
  | 'career';

// Example prompt
{
  "id": "write-blog-post-001",
  "title": "Blog Post Writer",
  "content": "Write a blog post about [TOPIC]. The post should be approximately [WORD_COUNT] words and include:\n\n1. An engaging hook in the introduction\n2. Clear subheadings for each main point\n3. Practical examples or case studies\n4. A compelling conclusion with a call to action\n\nTone: [TONE - e.g., professional, casual, educational]\nTarget audience: [AUDIENCE]\n\nStart with an outline, then write the full post.",
  "category": "writing",
  "tags": ["blog", "content", "seo"],
  "preview": "Write a blog post about [TOPIC]. The post should be approximately...",
  "useCases": ["Blog content", "Guest posts", "LinkedIn articles"],
  "tips": "Replace bracketed items with your specific details. Add examples from your industry for better results.",
  "createdAt": "2024-01-01",
  "updatedAt": "2024-01-15"
}
```

---

## API Routes

### GET /api/prompts

Returns all prompts from the library.

```typescript
// app/api/prompts/route.ts
import { NextResponse } from 'next/server';
import prompts from '@/data/prompts.json';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const category = searchParams.get('category');
  const search = searchParams.get('search');

  let filtered = prompts;

  if (category) {
    filtered = filtered.filter(p => p.category === category);
  }

  if (search) {
    // Use Fuse.js for fuzzy search
    const fuse = new Fuse(filtered, { keys: ['title', 'tags', 'content'] });
    filtered = fuse.search(search).map(r => r.item);
  }

  return NextResponse.json(filtered);
}
```

### POST /api/improve

Improves a user's prompt using AI.

```typescript
// app/api/improve/route.ts
import { NextResponse } from 'next/server';
import { createClient } from '@/lib/supabase/server';
import { openai } from '@/lib/openai';

export async function POST(request: Request) {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  // Check Pro status
  const { data: profile } = await supabase
    .from('profiles')
    .select('is_pro')
    .eq('id', user.id)
    .single();

  if (!profile?.is_pro) {
    return NextResponse.json({ error: 'Pro subscription required' }, { status: 403 });
  }

  // Rate limit check
  const { count } = await supabase
    .from('usage')
    .select('*', { count: 'exact' })
    .eq('user_id', user.id)
    .eq('action', 'improve')
    .gte('created_at', new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString());

  if (count >= 50) {
    return NextResponse.json({ error: 'Daily limit reached' }, { status: 429 });
  }

  const { prompt } = await request.json();

  const completion = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: [
      {
        role: 'system',
        content: IMPROVE_SYSTEM_PROMPT
      },
      {
        role: 'user',
        content: prompt
      }
    ],
    max_tokens: 2000
  });

  const improvedPrompt = completion.choices[0].message.content;

  // Log usage
  await supabase.from('usage').insert({
    user_id: user.id,
    action: 'improve'
  });

  // Save to history
  await supabase.from('prompt_history').insert({
    user_id: user.id,
    type: 'improve',
    input: prompt,
    output: improvedPrompt
  });

  return NextResponse.json({ improvedPrompt });
}
```

### POST /api/generate

Generates a new prompt from description.

```typescript
// app/api/generate/route.ts
// Similar structure to /api/improve
// Uses GENERATE_SYSTEM_PROMPT instead
```

---

## OpenAI Integration

```typescript
// lib/openai.ts
import OpenAI from 'openai';

export const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

export const IMPROVE_SYSTEM_PROMPT = `You are a prompt engineering expert. Your task is to improve the user's prompt to get better results from AI assistants.

Analyze the given prompt and improve it by:
1. Adding clear context and constraints
2. Specifying the desired output format
3. Including relevant examples if helpful
4. Breaking complex requests into steps
5. Removing ambiguity

Keep the improved prompt concise but complete. Output only the improved prompt, no explanation.`;

export const GENERATE_SYSTEM_PROMPT = `You are a prompt engineering expert. Create an effective prompt based on the user's description of what they want to accomplish.

The prompt should:
1. Be specific and actionable
2. Include context and constraints
3. Specify desired output format
4. Be ready to copy-paste into ChatGPT or Claude

Output only the prompt, no explanation.`;
```

---

## Stripe Integration (Web)

```typescript
// lib/stripe.ts
import Stripe from 'stripe';

export const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16'
});

export const PLANS = {
  monthly: {
    priceId: 'price_xxx_monthly',
    amount: 1900, // $19
    interval: 'month'
  },
  annual: {
    priceId: 'price_xxx_annual',
    amount: 9900, // $99/year
    interval: 'year'
  }
};
```

### Webhook Handler

```typescript
// app/api/webhooks/stripe/route.ts
import { stripe } from '@/lib/stripe';
import { createClient } from '@/lib/supabase/admin';

export async function POST(request: Request) {
  const body = await request.text();
  const signature = request.headers.get('stripe-signature')!;

  const event = stripe.webhooks.constructEvent(
    body,
    signature,
    process.env.STRIPE_WEBHOOK_SECRET!
  );

  const supabase = createClient();

  switch (event.type) {
    case 'checkout.session.completed':
      const session = event.data.object;
      await supabase
        .from('profiles')
        .update({ is_pro: true, subscription_status: 'active' })
        .eq('stripe_customer_id', session.customer);
      break;

    case 'customer.subscription.deleted':
      const subscription = event.data.object;
      await supabase
        .from('profiles')
        .update({ is_pro: false, subscription_status: 'canceled' })
        .eq('stripe_customer_id', subscription.customer);
      break;
  }

  return new Response('OK');
}
```

---

## Mobile App (React Native)

### File Structure

```
promptvault-mobile/
├── src/
│   ├── screens/
│   │   ├── HomeScreen.tsx
│   │   ├── SearchScreen.tsx
│   │   ├── CategoryScreen.tsx
│   │   ├── PromptDetailScreen.tsx
│   │   ├── ImproveScreen.tsx
│   │   ├── GenerateScreen.tsx
│   │   ├── FavoritesScreen.tsx
│   │   ├── HistoryScreen.tsx
│   │   ├── SettingsScreen.tsx
│   │   └── PaywallScreen.tsx
│   ├── components/
│   │   ├── PromptCard.tsx
│   │   ├── SearchBar.tsx
│   │   ├── CategoryChip.tsx
│   │   └── CopyButton.tsx
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── subscription.ts
│   ├── stores/
│   │   ├── authStore.ts
│   │   ├── promptStore.ts
│   │   └── favoriteStore.ts
│   └── App.tsx
├── ios/
├── android/
└── package.json
```

### API Service

```typescript
// services/api.ts
const API_URL = 'https://promptvault.com/api';

export async function getPrompts(category?: string) {
  const url = category
    ? `${API_URL}/prompts?category=${category}`
    : `${API_URL}/prompts`;
  const response = await fetch(url);
  return response.json();
}

export async function improvePrompt(prompt: string, token: string) {
  const response = await fetch(`${API_URL}/improve`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ prompt })
  });
  return response.json();
}

export async function generatePrompt(description: string, token: string) {
  const response = await fetch(`${API_URL}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({ description })
  });
  return response.json();
}
```

---

## Search Implementation

```typescript
// lib/search.ts
import Fuse from 'fuse.js';
import type { Prompt } from '@/types';

const fuseOptions = {
  keys: [
    { name: 'title', weight: 0.4 },
    { name: 'tags', weight: 0.3 },
    { name: 'content', weight: 0.2 },
    { name: 'useCases', weight: 0.1 }
  ],
  threshold: 0.4,
  includeScore: true
};

export function searchPrompts(prompts: Prompt[], query: string) {
  if (!query.trim()) return prompts;

  const fuse = new Fuse(prompts, fuseOptions);
  return fuse.search(query).map(result => result.item);
}
```

---

## Cost Estimation

### OpenAI API Costs

| Model | Input (1M tokens) | Output (1M tokens) |
|-------|-------------------|-------------------|
| GPT-4o-mini | $0.15 | $0.60 |

**Per improvement (avg 200 input + 500 output tokens):**
- Input: 200/1M * $0.15 = $0.00003
- Output: 500/1M * $0.60 = $0.0003
- Total per request: ~$0.0003

**Monthly at scale (10,000 requests):**
- 10,000 * $0.0003 = $3/month

### Monthly Costs at 1,000 Users

| Service | Cost |
|---------|------|
| Vercel | Free tier |
| Supabase | Free tier |
| OpenAI (5k requests) | ~$1.50 |
| Stripe (transactions) | 2.9% + $0.30 per |
| Domain | ~$1 |
| **Total** | ~$5/month |

Scales well due to:
- Free tier usage
- Efficient GPT-4o-mini model
- Client-side search (no API for browse)

---

## Security

### Authentication
- Supabase Auth (email, OAuth)
- Row Level Security on all tables
- JWT tokens for API auth

### Rate Limiting
- 50 AI requests per day (Pro)
- 1000 API calls per day (general)
- Implemented via database counts

### API Security
- API routes check auth
- Pro features check subscription
- Input validation on all endpoints

---

## Performance

### Targets
| Metric | Target |
|--------|--------|
| Time to first prompt | < 1s |
| Search response | < 100ms |
| AI improvement | < 5s |
| Page load (LCP) | < 2.5s |

### Optimization
- Static prompt data (no DB query for browse)
- Client-side search (Fuse.js)
- ISR for landing pages
- Edge functions for API routes

---

## Deployment

### Web (Vercel)
```bash
# Install
npm install

# Dev
npm run dev

# Deploy
vercel --prod
```

### Mobile (App Stores)
- Use EAS Build (Expo Application Services)
- TestFlight for iOS beta
- Internal track for Android beta

### Environment Variables
```
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# OpenAI
OPENAI_API_KEY=

# Stripe
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=

# RevenueCat (mobile)
REVENUECAT_API_KEY=
```

---

## Testing

### Unit Tests
- Prompt search logic
- Category filtering
- Data transformations

### Integration Tests
- API routes with mocked Supabase
- Stripe webhook handling
- OpenAI responses

### E2E Tests
- User signup flow
- Browse and copy prompt
- Improve prompt (with mock)
- Subscription purchase

---

## Chrome Extension (Phase 2)

Quick access to PromptVault from any page.

### Features
- Search prompts from popup
- One-click insert into ChatGPT text box
- Quick improve selection
- Favorites access

### Tech
- Manifest V3
- React for popup
- Content script for injection
- Same API endpoints
