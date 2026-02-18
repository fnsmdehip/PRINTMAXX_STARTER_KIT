# AI Wrapper Quickstart Template

**Time to MVP:** 3-7 days
**Cost:** $0-50
**Stack:** Next.js + OpenAI API + Stripe + Vercel

---

## Day 1: Setup + Landing Page

### 1. Project Setup

```bash
# Create Next.js app
npx create-next-app@latest my-ai-wrapper --typescript --tailwind --app

# Install dependencies
cd my-ai-wrapper
npm install openai stripe @stripe/stripe-js
```

### 2. Environment Variables

Create `.env.local`:
```
OPENAI_API_KEY=sk-...
STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### 3. Landing Page Structure

```
app/
├── page.tsx           # Landing page
├── app/
│   └── page.tsx       # Main app (after login)
├── api/
│   ├── generate/
│   │   └── route.ts   # AI generation endpoint
│   └── checkout/
│       └── route.ts   # Stripe checkout
└── components/
    ├── Hero.tsx
    ├── Features.tsx
    ├── Pricing.tsx
    └── Generator.tsx
```

---

## Day 2: Core AI Feature

### API Route (`app/api/generate/route.ts`)

```typescript
import OpenAI from 'openai';
import { NextRequest, NextResponse } from 'next/server';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

// Your niche-specific system prompt
const SYSTEM_PROMPT = `You are an expert [NICHE] content creator.

Your outputs should be:
- [Quality 1]
- [Quality 2]
- [Quality 3]

Format: [Specify format]
`;

export async function POST(req: NextRequest) {
  try {
    const { input, template } = await req.json();

    // TODO: Add rate limiting and auth check here

    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini", // Cheap, fast, good enough
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        { role: "user", content: buildPrompt(input, template) }
      ],
      max_tokens: 1000,
      temperature: 0.7,
    });

    const output = completion.choices[0].message.content;

    return NextResponse.json({ output });
  } catch (error) {
    console.error('Generation error:', error);
    return NextResponse.json(
      { error: 'Generation failed' },
      { status: 500 }
    );
  }
}

function buildPrompt(input: string, template: string): string {
  // Template-specific prompt construction
  const templates = {
    'template1': `Create a [output type] about: ${input}`,
    'template2': `Based on this input, generate: ${input}`,
  };

  return templates[template] || `Process this: ${input}`;
}
```

### Frontend Component (`components/Generator.tsx`)

```typescript
'use client';

import { useState } from 'react';

export function Generator() {
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleGenerate() {
    setLoading(true);
    try {
      const res = await fetch('/api/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input, template: 'template1' }),
      });

      const data = await res.json();
      setOutput(data.output);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">[Your Tool Name]</h2>

      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Enter your [input type]..."
        className="w-full h-32 p-4 border rounded-lg mb-4"
      />

      <button
        onClick={handleGenerate}
        disabled={loading || !input}
        className="w-full py-3 bg-blue-600 text-white rounded-lg disabled:opacity-50"
      >
        {loading ? 'Generating...' : 'Generate'}
      </button>

      {output && (
        <div className="mt-6 p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold mb-2">Output:</h3>
          <div className="whitespace-pre-wrap">{output}</div>
        </div>
      )}
    </div>
  );
}
```

---

## Day 3: Payments

### Stripe Checkout (`app/api/checkout/route.ts`)

```typescript
import Stripe from 'stripe';
import { NextRequest, NextResponse } from 'next/server';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!);

export async function POST(req: NextRequest) {
  const { priceId, userId } = await req.json();

  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    payment_method_types: ['card'],
    line_items: [{ price: priceId, quantity: 1 }],
    success_url: `${process.env.NEXT_PUBLIC_APP_URL}/app?success=true`,
    cancel_url: `${process.env.NEXT_PUBLIC_APP_URL}?canceled=true`,
    metadata: { userId },
  });

  return NextResponse.json({ url: session.url });
}
```

### Pricing Plans (Stripe Dashboard)

Create these products in Stripe:
- **Basic:** $9/mo - 50 generations
- **Pro:** $29/mo - 500 generations
- **Unlimited:** $79/mo - Unlimited (soft cap)

---

## Day 4-5: Polish + Deploy

### Rate Limiting (Simple Version)

```typescript
// lib/rateLimit.ts
const userGenerations: Map<string, number> = new Map();

export function checkRateLimit(userId: string, plan: string): boolean {
  const limits = {
    free: 5,      // per day
    basic: 50,
    pro: 500,
    unlimited: 2000,
  };

  const current = userGenerations.get(userId) || 0;
  const limit = limits[plan] || 5;

  if (current >= limit) {
    return false;
  }

  userGenerations.set(userId, current + 1);
  return true;
}
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel

# Set environment variables in Vercel dashboard
# OPENAI_API_KEY, STRIPE_SECRET_KEY, etc.
```

---

## Day 6-7: Launch

### Pre-Launch Checklist

- [ ] Landing page live
- [ ] Core feature working
- [ ] Payments working (test with Stripe test mode)
- [ ] Error handling
- [ ] Mobile responsive
- [ ] Analytics (Vercel Analytics or Mixpanel)
- [ ] Terms of Service page
- [ ] Privacy Policy page

### Launch Channels

1. **Product Hunt** - Prep assets, get hunter
2. **Twitter/X** - Thread explaining what you built
3. **Reddit** - r/SideProject, niche subreddits
4. **Hacker News** - Show HN post
5. **Indie Hackers** - Launch post
6. **Niche communities** - Discord, Facebook groups

### Launch Week Tasks

- [ ] Post to all channels Day 1
- [ ] Respond to all comments/questions
- [ ] Fix bugs immediately
- [ ] Collect testimonials from early users
- [ ] Set up email capture for non-converters
- [ ] Start content marketing

---

## Cost Tracking Template

```
| Item | Monthly Cost | Notes |
|------|--------------|-------|
| Vercel Hosting | $0-20 | Free tier works for launch |
| OpenAI API | Variable | ~$0.01-0.05 per generation |
| Stripe | 2.9% + $0.30 | Per transaction |
| Domain | ~$1/mo | Annual cost ~$12 |
| Email (Resend) | $0-20 | Free tier for launch |
| TOTAL | ~$20-50 | Before revenue |
```

## Revenue Math

```
Target: $1k MRR

At $29/mo:
- Need 35 paying users
- At 3% free-to-paid conversion
- Need ~1,200 free users
- At 10% visitor-to-signup
- Need ~12,000 visitors

Acquisition math:
- 10 pieces of content
- Each gets 1,200 views avg
- = 12,000 visitors
- = 1,200 signups
- = 35 paid users
- = $1k MRR
```

---

## Template Customization by Niche

### Faith Wrapper (SermonGen)

System Prompt:
```
You are an expert sermon writer with deep knowledge of the Bible.
Create sermon outlines that are:
- Biblically accurate with scripture references
- Practical with real-life applications
- Structured with clear points (typically 3)
- Appropriate length for [denomination] services

Output format: Title, Opening, 3 Main Points with sub-points, Application, Closing
```

### Cold Email Wrapper (ColdMailMaxx)

System Prompt:
```
You are an expert cold email copywriter using the 6-question framework.
Every email must answer:
1. What do you do?
2. Who do you do it for?
3. How do you do it?
4. What problem do you solve?
5. What's your proof?
6. What's the ROI?

Format: Under 100 words, plain text, no formatting, clear CTA
```

### Fitness Wrapper (FitCoach AI)

System Prompt:
```
You are a certified personal trainer and nutritionist.
Create workout/meal plans that are:
- Safe and appropriate for fitness level
- Achievable with available equipment
- Progressive toward stated goals
- Balanced for nutrition and recovery

Output: Weekly plan with daily breakdowns, sets/reps, rest times
```

---

## Next Steps After Launch

1. **Week 1-2:** Fix bugs, respond to users
2. **Week 2-4:** Add most-requested features
3. **Month 2:** Content marketing ramp-up
4. **Month 3:** Consider paid acquisition if unit economics work
5. **Month 6:** Evaluate expand or double down

The goal is $1k MRR in 30 days. If you hit it, scale. If not, iterate or pivot.
