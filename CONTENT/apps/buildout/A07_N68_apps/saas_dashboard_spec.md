# SaaS Dashboard — Feature Spec

**Concept:** A unified revenue and operations dashboard for solopreneurs running multiple income streams. Connect Stripe, Gumroad, Lemon Squeezy, Shopify, AdSense, Beehiiv, and 15+ other sources — one clean view of your entire business in real time.

**Target User:** Solopreneurs with 2-10 income streams who waste 30 min/day manually checking dashboards. $1K-$20K/mo revenue range.

**Category:** Business / Finance
**Platform:** Web app (Next.js) + iOS/Android native (Phase 2)
**Pricing:**
- Starter: Free (2 integrations)
- Pro: $19/mo (unlimited integrations + alerts + goals)
- Team: $49/mo (3 seats + shared dashboard)

**Revenue Target:** $5,000/mo at 263 Pro subs — achievable at 10K signups with 2.6% conversion

---

## Core Differentiator

Existing tools (Baremetrics, ChartMogul) are enterprise-only and MRR-focused. They cost $50-200/mo and only work for pure SaaS. PromptMaxx Dashboard works for the mixed-income solopreneur: Stripe + Gumroad + Shopify + AdSense + affiliate networks + freelance invoices — all in one view at $19/mo.

---

## MVP Features (v1.0)

### 1. Revenue Overview
- Total revenue today / this week / this month / this year
- MoM growth rate (e.g., "+23% vs last month")
- Revenue by source (pie chart + bar chart)
- Daily revenue chart (last 30 days, 90 days, 1 year)
- Projections: run-rate MRR, projected month-end based on current pace
- Net revenue: gross minus platform fees (calculated automatically per integration)

### 2. Integrations (Phase 1 — MVP)

| Platform | What We Pull | Method |
|---|---|---|
| Stripe | charges, refunds, subscriptions, MRR | Stripe API |
| Gumroad | sales, products, refunds | Gumroad API |
| Lemon Squeezy | orders, subscriptions | LS API |
| Shopify | orders, refunds, abandoned cart rate | Shopify API |
| Google AdSense | estimated earnings, RPM, pageviews | AdSense Reporting API |
| Beehiiv | subscribers, revenue, paid sub count | Beehiiv API |
| PayPal | transactions, refunds | PayPal REST API |
| Wise | balance, incoming transactions | Wise API |

**Phase 2 integrations:**
- Amazon Associates (affiliate earnings)
| ClickBank | ShareASale | Impact | CJ Affiliate
- Substack (subscriber count, paid subs)
- Ko-fi (donations, shop sales)
- Etsy (orders, revenue)
- TikTok Shop (orders, commissions)
- Custom webhook (any source with JSON webhook)

### 3. Goals & Alerts
- Set monthly revenue goal per stream or total
- Progress bar toward goal on dashboard
- Alerts (email + push):
  - "First sale of the day" notification
  - "You're 80% to your monthly goal"
  - "Revenue down 30% from yesterday"
  - "New subscriber spike (+50 in 1 hour)"
  - "Refund rate above 5%"
- Milestone celebrations: $1K day, $10K month, $100K year

### 4. Transaction Feed
- All transactions from all sources in one unified feed
- Columns: time, source (Stripe/Gumroad/etc.), product, amount, net amount, type (sale/refund/subscription)
- Filter by: source, type, date range, product
- Export: CSV
- Search by customer email, product name, amount

### 5. Products Dashboard
- All products/listings across all platforms in one table
- Revenue per product (all-time, this month)
- Conversion rate where available (Shopify, Stripe)
- Best performers ranked by revenue
- Products with zero sales in 30 days flagged

### 6. Expense Tracking (manual)
- Add expenses manually: category, amount, date, notes, recurring toggle
- Categories: SaaS tools, ads, contractors, hosting, misc
- Profit/loss: revenue - expenses per month
- Expense vs revenue chart
- Tax estimate: calculate estimated quarterly tax owed (US 25-30% bracket)

---

## Advanced Features (Pro)

### 7. Cohort Analysis
- New customers by month (cohort view)
- Retention: do customers buy again within 30/60/90 days?
- LTV by acquisition source (if tracked via UTM)

### 8. Competitor Benchmarking
- Anonymous community benchmarks: "solopreneurs at your revenue level average X% MoM growth"
- Opt-in: share your anonymized data, get benchmarks back
- Percentile ranking: "you're in the top 30% of solopreneurs at $5K-$15K/mo MRR"

### 9. AI Insights (Claude API)
- Weekly digest email: "Here's what happened this week and what I'd focus on"
- Anomaly detection: "Your Gumroad sales dropped 40% — your most recent product got a 2-star review"
- Opportunity flags: "Your AdSense RPM doubled this week — traffic spike from [source]"
- Powered by Claude Haiku (cheap, fast) — COGS ~$0.02/insight

### 10. Public Revenue Page (optional)
- User can publish their revenue journey publicly (like levels.io/revenue)
- Custom URL: dashboard.printmaxx.com/u/username
- Build in public social proof — drives organic signups
- Toggle on/off, choose which streams to show

---

## Technical Architecture

### Stack
```
Frontend:  Next.js 14 + TypeScript + Tailwind + Recharts (charts) + shadcn/ui
Backend:   Next.js API routes + Supabase (Postgres + Auth)
Jobs:      Vercel Cron (pull integration data every 15 min)
Queue:     Supabase pg_cron for scheduled sync jobs
Cache:     Redis (Upstash) — cache integration responses 5 min
Payments:  Stripe (subscriptions)
AI:        Anthropic Claude Haiku (insights)
Deploy:    Vercel
```

### Integration Architecture
```typescript
// Each integration follows this interface
interface Integration {
  id: string;
  name: string;
  logo: string;
  authType: 'api_key' | 'oauth2';

  connect(credentials: Record<string, string>): Promise<boolean>;
  syncRevenue(since: Date): Promise<Transaction[]>;
  getMetrics(): Promise<IntegrationMetrics>;
}

interface Transaction {
  id: string;
  source: string;  // 'stripe' | 'gumroad' | etc.
  amount: number;  // in cents
  currency: string;
  net_amount: number;  // after platform fees
  type: 'sale' | 'refund' | 'subscription' | 'payout';
  product_name?: string;
  customer_email?: string;
  created_at: Date;
}
```

### Stripe Integration Example
```typescript
import Stripe from 'stripe';

export class StripeIntegration implements Integration {
  private stripe: Stripe;

  constructor(secretKey: string) {
    this.stripe = new Stripe(secretKey, { apiVersion: '2024-12-18.acacia' });
  }

  async syncRevenue(since: Date): Promise<Transaction[]> {
    const charges = await this.stripe.charges.list({
      created: { gte: Math.floor(since.getTime() / 1000) },
      limit: 100,
    });

    return charges.data.map(charge => ({
      id: charge.id,
      source: 'stripe',
      amount: charge.amount,
      currency: charge.currency,
      net_amount: charge.amount - (charge.application_fee_amount || 0),
      type: charge.refunded ? 'refund' : 'sale',
      product_name: charge.description || undefined,
      customer_email: charge.billing_details?.email || undefined,
      created_at: new Date(charge.created * 1000),
    }));
  }
}
```

### Database Schema (key tables)
```sql
CREATE TABLE integrations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users NOT NULL,
  platform TEXT NOT NULL,  -- 'stripe', 'gumroad', etc.
  credentials JSONB,  -- encrypted at rest via Supabase vault
  last_synced_at TIMESTAMPTZ,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE transactions (
  id TEXT PRIMARY KEY,  -- platform-native ID
  user_id UUID REFERENCES auth.users NOT NULL,
  integration_id UUID REFERENCES integrations(id) NOT NULL,
  source TEXT NOT NULL,
  amount INTEGER NOT NULL,  -- cents
  currency TEXT DEFAULT 'usd',
  net_amount INTEGER,
  type TEXT NOT NULL,
  product_name TEXT,
  customer_email TEXT,
  created_at TIMESTAMPTZ NOT NULL,
  synced_at TIMESTAMPTZ DEFAULT now()
);

-- Index for fast dashboard queries
CREATE INDEX idx_transactions_user_date ON transactions(user_id, created_at DESC);
CREATE INDEX idx_transactions_source ON transactions(user_id, source, created_at DESC);
```

---

## Security (Critical — handles financial credentials)

- API keys stored encrypted via Supabase Vault (AES-256)
- Keys never returned to frontend after initial save (write-only)
- All API calls to integrations happen server-side only
- OAuth flows: tokens stored encrypted, refresh server-side
- Rate limiting on all sync endpoints (prevent credential abuse)
- SOC2 path: document controls from day 1

---

## Pricing & Revenue Math

| Plan | Price | Integrations | Alerts | Seats |
|---|---|---|---|---|
| Starter | $0 | 2 | Email only | 1 |
| Pro | $19/mo | Unlimited | Email + Push | 1 |
| Team | $49/mo | Unlimited | Email + Push | 3 |

**Revenue projections:**
| Metric | Month 3 | Month 6 | Month 12 |
|---|---|---|---|
| Free signups | 500 | 1,500 | 5,000 |
| Pro conversion | 2% | 3% | 4% |
| Pro subs | 10 | 45 | 200 |
| Team subs | 2 | 8 | 30 |
| MRR | $290 | $1,245 | $5,270 |

**Cost base:**
- Vercel Pro: $20/mo
- Supabase Pro: $25/mo
- Upstash Redis: $10/mo
- Claude Haiku (insights): ~$20/mo at 200 users
- Total: ~$75/mo

**Break-even:** 4 Pro subs. Profitable from first week.

---

## Competitive Analysis

| Tool | Price | Multi-source | Non-SaaS support | Solopreneur focus |
|---|---|---|---|---|
| Baremetrics | $50-200/mo | Stripe only | No | No |
| ChartMogul | $100/mo+ | Limited | No | No |
| ProfitWell | $100/mo | Stripe/Braintree | No | No |
| Notion dashboards | Manual | Manual | Manual | DIY |
| **SaaS Dashboard** | **$19/mo** | **15+ sources** | **Yes (Gumroad, AdSense, etc.)** | **Yes** |

---

## Launch Plan

**Week 1-2:** Core MVP — Stripe + Gumroad + chart UI
**Week 3:** Beehiiv + AdSense integrations
**Week 4:** Goals + alerts + launch

**Distribution:**
- Product Hunt: "one dashboard for your entire indie business"
- r/SideProject, r/indiehackers, r/SaaS launch posts
- IndieHackers.com featured story: "I built this to stop switching between 8 tabs"
- Twitter/X thread: show dashboard screenshot with real numbers (build-in-public)
- Beehiiv newsletter feature: reach newsletter operators

**Hook for Twitter:**
"I was checking 8 different dashboards every morning. Stripe. Gumroad. AdSense. Shopify. Beehiiv. Took 30 minutes. I built one dashboard that pulls all of it. Free to try."

---

## Build Timeline

| Phase | Duration | Deliverable |
|---|---|---|
| Auth + UI shell | Week 1 | Next.js app with Supabase auth |
| Stripe integration | Week 2 | Revenue chart from Stripe |
| Gumroad + AdSense | Week 3 | Multi-source dashboard |
| Goals + alerts | Week 4 | Email notifications |
| Stripe billing | Week 4 | Pro subscription gate |
| Launch | Week 5 | Product Hunt |
| Additional integrations | Ongoing | 1 new per week |
