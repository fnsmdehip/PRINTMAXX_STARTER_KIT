# AI Wrapper Quick Start: From Idea to $10K MRR in 12 Weeks

**This guide:** Step-by-step to launch your first AI wrapper and validate product-market fit.

---

## Phase 1: Planning (Days 1-3)

### Pick Your Niche
- Answer: Who is your target user? What's their main pain point?
- Reference: `AI_WRAPPER_IDEAS_ALL_NICHES.md` (pick top 3 options)
- Interview 5 potential users: "Would you pay $X/mo for this?"

### Define Your MVP
- Pick 2-3 core features ONLY (not 10)
- Example: WorkoutFormChecker MVP = video upload + form analysis + feedback
- List exact APIs you'll use (Claude, Twilio, Stripe, etc.)

### Landing Page Draft
- Headline: "[Problem] solved in [Time]"
- Subhead: Who it's for + why it's different
- CTA: "Early access $X/mo discount"
- Example: "Form feedback in 30 seconds. AI trainer for $7.99/mo"

---

## Phase 2: Quick Build (Days 4-14)

### Day 4-5: Setup
```bash
# Create Next.js project
npx create-next-app@latest my-wrapper --typescript --tailwind

# Install dependencies
npm install @anthropic-ai/sdk stripe @supabase/supabase-js

# Set up environment
cp .env.example .env.local
# Add: ANTHROPIC_API_KEY, STRIPE_KEY, DATABASE_URL
```

### Day 6-10: Core Feature
**Example: Simple Wrapper (Form Checker)**

```typescript
// app/api/analyze-form/route.ts
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

export async function POST(request: Request) {
  const { videoUrl, exerciseName } = await request.json();

  // Placeholder: In real implementation, analyze video with Claude Vision
  const message = await client.messages.create({
    model: "claude-3-5-sonnet-20241022",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: `Analyze gym form for: ${exerciseName}. Video URL: ${videoUrl}. Give: (1) Form grade A-F, (2) 3 specific fixes, (3) Injury risks`,
      },
    ],
  });

  return Response.json(message.content[0]);
}
```

### Day 11-12: Payments + Auth
```typescript
// Use Stripe for subscriptions
// Use NextAuth for simple auth (GitHub, Google)
// Use Supabase for database (users, usage tracking)
```

### Day 13-14: Landing Page
- Deploy to Vercel (1 click)
- Add Stripe Subscribe button
- Setup email collection (ConvertKit, Substack)

---

## Phase 3: Soft Launch (Days 15-21)

### Day 15: Launch to 3 Communities
1. **Reddit** - Post to relevant subreddit
   - Example: r/fitness (WorkoutFormChecker)
   - Message: "I built AI form analysis. Early access 50% off?"

2. **Discord** - Indie hackers, niche Discord communities
   - IndieHackers, relevant hobby servers

3. **Email list** - If you have one (or swap with partners)

### Day 16-19: Gather Feedback
- Ask early users: "What's missing? Would you pay $X?"
- Iterate based on feedback (not feature creep)
- Fix bugs immediately

### Day 20: Iterate
- Price test: Ask 5 users if $7.99 is right price
- Feature test: Which feature is 90% of value? Keep. Others? Cut.
- UX test: Can people understand how to use it in <2 minutes?

### Day 21: Measure
- Signups: What's your conversion rate? (Target: 1%)
- Retention: % still using after 3 days? (Target: 50%+)
- NPS: Would they recommend? (Target: 30+)

---

## Phase 4: Paid Growth (Weeks 4-8)

### Week 4: Referral Program
- Offer: $20 credit if friend subscribes
- Viral loop: Every user can share referral link
- Track: Coefficient of viral growth

### Week 5-6: Paid Ads
- Start with $500/month budget
- Platforms: Twitter Ads (best for B2C), Reddit Ads (communities)
- Message: "Save $X/month vs alternatives" or "Finally AI that..."
- Target: 3:1 LTV:CAC ratio

### Week 7-8: Content
- Blog: "How to do X better" (SEO traffic)
- Twitter: Daily tips using your wrapper
- Video: 1-2 min demo video (TikTok/YouTube)

---

## Phase 5: Scale (Weeks 9-12)

### By Week 12 Goal
- Monthly Recurring Revenue: $10K+
- Monthly Active Users: 1,000+
- Customer Acquisition Cost: <$30
- Lifetime Value: >$200
- Churn Rate: <40% monthly

### To Hit $10K MRR
- Option A: 500 users @ $20/mo
- Option B: 200 users @ $50/mo
- Option C: 100 users @ $100/mo (premium tier)

### At Week 12, Decide:
1. **Scaling direction:** Keep growing this wrapper or add adjacent features?
2. **New wrapper:** Launch wrapper #2 while #1 runs on autopilot
3. **Acquisition:** Hire for sales/marketing or stay scrappy?

---

## Real Numbers: WorkoutFormChecker Example

### Week 1
- Landing page live
- 10 signups (friends + Reddit)
- 0 paid conversions

### Week 2-3
- 50 total signups
- 5 paid conversions ($40 MRR)
- Feedback: "Form analysis not accurate enough"
- Fix: Improve Claude prompts

### Week 4-6
- 200 total signups
- 40 paid ($320 MRR)
- Launch referral program (+15 signups/week)
- Paid ads test ($500 spend, 10 customers = $100 MRR)

### Week 7-9
- 600 total signups
- 120 paid ($960 MRR)
- Scale ads to $2K/week (60 new customers/week)
- Revenue: $5K+ MRR

### Week 10-12
- 1,500 total signups
- 300 paid ($2,400 MRR)
- Continued ads + viral referrals
- Revenue: $10K+ MRR

---

## Common Mistakes (Avoid These)

### ❌ Building too many features
- Solution: Ship MVP with 2-3 features. Add based on demand only

### ❌ Targeting "everyone"
- Solution: Pick one specific user (ADHD adults, gym-goers, etc). They'll tell their friends

### ❌ Underpricing
- Solution: Charge $9.99+ (low prices attract wrong customers, high prices attract serious users)

### ❌ No clear differentiation
- Solution: "Better than ChatGPT at X" not "just another AI wrapper"

### ❌ Patience with iterations
- Solution: Show early users every week. Ship fast, iterate based on feedback

### ❌ Building without talking to users
- Solution: Interview 10 potential users before coding. Interview 10 early users weekly

---

## API Cost Breakdown (Per Wrapper, Monthly)

| API | Cost | Usage |
|-----|------|-------|
| Claude API | $100-500 | 10K-50K calls |
| Stripe | 2.9% + $0.30 | Payment processing |
| Supabase | $25-100 | Database + auth |
| Vercel | $20 | Hosting |
| Email (SendGrid) | $10-50 | 10K-100K emails |
| ElevenLabs | $10-100 | Voice generation |
| **Total** | **$200-800** | -- |

**At $20 ARPU with 100 users = $2K revenue, $500 API costs = $1.5K profit**

---

## Quick API Integration Checklist

### Claude API (Core Intelligence)
```javascript
const message = await client.messages.create({
  model: "claude-3-5-sonnet-20241022",
  max_tokens: 1024,
  messages: [{role: "user", content: userInput}]
});
```

### Stripe (Payments)
```javascript
// Create subscription
const subscription = await stripe.subscriptions.create({
  customer: customerId,
  items: [{price: 'price_123'}],
});
```

### Supabase (Database)
```javascript
// Insert user
const { data } = await supabase
  .from('users')
  .insert([{email, name}]);
```

### Email (ConvertKit/SendGrid)
```javascript
// Send welcome email
await sendEmail({
  to: userEmail,
  template: 'welcome',
  data: {name}
});
```

---

## Go-to-Market Playbook (Per Niche)

### Tech Workers (N001, N006, N016)
- **Where:** Twitter, Reddit r/programming, Indie Hackers
- **Message:** "Save X hours/week" + "Better than [competitor]"
- **Content:** Technical deep-dives, comparisons

### Health/Wellness (N003, N005, N009, N011, N022, N023, N025, N026)
- **Where:** TikTok, Instagram, health communities
- **Message:** "Finally [solution] for [problem]"
- **Content:** Success stories, before-after

### Service Businesses (N031, N033)
- **Where:** LinkedIn, industry email lists, trade shows
- **Message:** "ROI in 30 days" + hard numbers
- **Content:** Case studies, webinars

### Creators (N032)
- **Where:** TikTok, YouTube, creator communities
- **Message:** "Passive income from [platform]"
- **Content:** Revenue breakdowns, opportunity analysis

---

## Key Metrics Dashboard

Track these every week:

```
Week X:
- Signups: [count]
- Paid conversions: [count] @ [price]
- MRR: $[amount]
- CAC: $[amount]
- LTV: $[amount]
- Free-to-paid conversion: [%]
- Retention (7-day): [%]
- NPS: [score]

Key insight: [biggest learning]
Next week's focus: [priority]
```

---

## Timeline to $100K MRR (All 5 Wrappers)

| Month | Wrapper 1 MRR | Wrapper 2 MRR | Wrapper 3 MRR | Wrapper 4 MRR | Wrapper 5 MRR | Total |
|-------|---------------|---------------|---------------|---------------|---------------|--------|
| Month 1 | $5K | -- | -- | -- | -- | $5K |
| Month 2 | $15K | $3K | -- | -- | -- | $18K |
| Month 3 | $25K | $10K | $5K | -- | -- | $40K |
| Month 4 | $35K | $20K | $12K | $3K | -- | $70K |
| Month 5 | $45K | $30K | $18K | $10K | $2K | $105K |

---

## Resource Links

**Building:**
- Next.js docs: nextjs.org
- Anthropic Claude API: docs.anthropic.com
- Supabase docs: supabase.com/docs
- Stripe docs: stripe.com/docs

**Marketing:**
- Product Hunt: producthunt.com (launch)
- Indie Hackers: indiehackers.com (community)
- Twitter API: developer.twitter.com

**Design:**
- Shadcn UI: shadcn-ui.com (components)
- Tailwind CSS: tailwindcss.com
- Vercel: vercel.com (hosting)

**Landing Pages:**
- Carrd.co (simple)
- Webflow (advanced)
- Next.js App Router (full control)

---

## Success is Determined By:

1. **Problem clarity** (50%) - Do users have this pain daily? Would they pay?
2. **Solution timing** (30%) - Is AI the right tool? Is the market ready?
3. **Execution speed** (20%) - Can you ship working MVP in 2 weeks?

**You don't need:** Huge initial user base, perfect code, fancy design
**You need:** Real problem, working solution, early customers

---

**Start date:** This week
**First launch target:** 14 days
**First customers:** Day 15-21
**$10K MRR:** 12 weeks per wrapper

**Go build. 🚀**
