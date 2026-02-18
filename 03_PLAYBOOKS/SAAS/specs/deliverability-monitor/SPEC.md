# InboxGuard -- Email Deliverability Monitor

**Product Name:** InboxGuard
**Tagline:** "Never land in spam again. Monitor your domain health in real-time."
**Category:** Micro-SaaS (MM028) + Cold Outbound (MM007)
**Target:** Cold emailers, agencies, solopreneurs doing outbound

---

## Product Overview

InboxGuard monitors email domain health 24/7 and alerts when something breaks. DNS authentication (SPF/DKIM/DMARC), blacklist monitoring, inbox placement testing, and warmup tracking -- all in one dashboard. Built for cold emailers who can't afford to land in spam.

---

## MVP Features (5 Core)

### 1. Domain Health Scanner
- Input domain, get instant health score (0-100)
- Checks SPF record validity
- Checks DKIM configuration
- Checks DMARC policy
- Checks MX records
- Checks for common misconfigurations
- **Output:** Health score + specific fix recommendations

### 2. Blacklist Monitor
- Monitors 80+ email blacklists (Spamhaus, Barracuda, etc.)
- Checks every 6 hours automatically
- Instant alert (email + webhook) if domain appears on any blacklist
- Delisting instructions per blacklist
- Historical blacklist status log

### 3. Inbox Placement Tester
- Send test email to seed accounts (Gmail, Outlook, Yahoo, iCloud)
- Report: Inbox vs Spam vs Missing per provider
- Subject line analysis (spam trigger words)
- Authentication header analysis
- Weekly automated placement tests

### 4. Warmup Tracker
- Connect email accounts via IMAP
- Track daily send volume
- Monitor reply rates
- Warmup progress visualization
- Recommended daily send limits based on domain age + reputation
- Integration with common warmup tools (Instantly, Warmbox)

### 5. Alert System
- Email alerts for: blacklist hit, health score drop, placement degradation
- Webhook support for Slack/Discord/Zapier
- Daily health digest email
- Weekly report with trends
- Severity levels: Critical (blacklist), Warning (score drop), Info (weekly)

---

## Tech Stack

```
Frontend:
  - Next.js 16 (App Router)
  - Tailwind CSS + shadcn/ui
  - Chart.js for visualizations
  - React Query for data fetching

Backend:
  - Supabase (PostgreSQL, Auth, Edge Functions)
  - Supabase Cron for scheduled checks
  - Edge Functions for DNS lookups + blacklist checks

APIs:
  - dns.resolve() for SPF/DKIM/DMARC/MX lookups
  - Custom blacklist checker (HTTP requests to 80+ DNSBL)
  - IMAP for warmup tracking
  - Resend for alert emails
  - Stripe for subscriptions

Hosting:
  - Vercel (frontend)
  - Supabase (backend)

Monitoring:
  - PostHog (analytics)
  - Sentry (error tracking)
```

---

## Database Schema

```sql
-- Users
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  plan TEXT DEFAULT 'free', -- free, starter, pro, agency
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  created_at TIMESTAMPTZ DEFAULT now()
);

-- Domains
CREATE TABLE domains (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  domain TEXT NOT NULL,
  health_score INTEGER DEFAULT 0,
  spf_valid BOOLEAN,
  dkim_valid BOOLEAN,
  dmarc_valid BOOLEAN,
  mx_valid BOOLEAN,
  last_checked_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(user_id, domain)
);

-- Blacklist checks
CREATE TABLE blacklist_checks (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  domain_id UUID REFERENCES domains(id),
  blacklist_name TEXT NOT NULL,
  is_listed BOOLEAN DEFAULT false,
  checked_at TIMESTAMPTZ DEFAULT now()
);

-- Inbox placement tests
CREATE TABLE placement_tests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  domain_id UUID REFERENCES domains(id),
  gmail_result TEXT, -- inbox, spam, missing
  outlook_result TEXT,
  yahoo_result TEXT,
  icloud_result TEXT,
  subject_line TEXT,
  spam_triggers JSONB,
  tested_at TIMESTAMPTZ DEFAULT now()
);

-- Warmup tracking
CREATE TABLE warmup_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  domain_id UUID REFERENCES domains(id),
  date DATE NOT NULL,
  emails_sent INTEGER DEFAULT 0,
  replies_received INTEGER DEFAULT 0,
  bounce_count INTEGER DEFAULT 0,
  warmup_score INTEGER DEFAULT 0,
  UNIQUE(domain_id, date)
);

-- Alerts
CREATE TABLE alerts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  domain_id UUID REFERENCES domains(id),
  severity TEXT NOT NULL, -- critical, warning, info
  type TEXT NOT NULL, -- blacklist, health_drop, placement_drop
  message TEXT NOT NULL,
  resolved BOOLEAN DEFAULT false,
  created_at TIMESTAMPTZ DEFAULT now()
);
```

---

## API Endpoints

```
Auth:
POST /api/auth/signup
POST /api/auth/login
GET  /api/auth/me

Domains:
POST   /api/domains              -- Add domain to monitor
GET    /api/domains              -- List user's domains
GET    /api/domains/:id          -- Get domain details
DELETE /api/domains/:id          -- Remove domain
POST   /api/domains/:id/scan     -- Trigger manual scan

Health:
GET  /api/domains/:id/health     -- Current health score + details
GET  /api/domains/:id/health/history -- Health score over time

Blacklists:
GET  /api/domains/:id/blacklists -- Current blacklist status
GET  /api/domains/:id/blacklists/history -- Blacklist history

Placement:
POST /api/domains/:id/placement/test -- Run placement test
GET  /api/domains/:id/placement -- Recent placement results

Warmup:
POST /api/domains/:id/warmup/connect -- Connect IMAP
GET  /api/domains/:id/warmup -- Warmup stats
GET  /api/domains/:id/warmup/recommendations -- AI recommendations

Alerts:
GET  /api/alerts -- All alerts for user
PUT  /api/alerts/:id/resolve -- Mark alert resolved

Billing:
POST /api/billing/checkout -- Create Stripe checkout
POST /api/billing/portal -- Stripe customer portal
POST /api/billing/webhook -- Stripe webhook handler
```

---

## Pricing Model

| Feature | Free | Starter ($19/mo) | Pro ($49/mo) | Agency ($99/mo) |
|---------|------|-------------------|--------------|-----------------|
| Domains | 1 | 3 | 10 | 25 |
| Health checks | Daily | Every 6 hours | Hourly | Every 15 min |
| Blacklist monitoring | 20 lists | 50 lists | 80+ lists | 80+ lists |
| Placement tests | 1/week | 3/week | Daily | Unlimited |
| Warmup tracking | No | 1 account | 5 accounts | 20 accounts |
| Alerts | Email only | Email + webhook | All channels | All + custom |
| API access | No | No | Yes | Yes |
| White-label reports | No | No | No | Yes |

---

## Landing Page Copy

### Hero

**Headline:** Stop landing in spam.
**Subheadline:** InboxGuard monitors your email domain health 24/7. SPF, DKIM, DMARC, blacklists, inbox placement -- all in one dashboard. Know the second something breaks.

### Pain Points

- "My open rates dropped 40% and I didn't know why for 2 weeks"
- "I was on 3 blacklists and had no idea"
- "My SPF record was misconfigured for months"
- "My warmup tool stopped working and I sent to spam for a week"

### Features (Benefit-first)

1. **Domain health score** -- One number tells you if you're good or broken
2. **Blacklist alerts** -- Know within 6 hours if you hit a blacklist
3. **Inbox placement tests** -- See exactly where your emails land
4. **Warmup tracking** -- Visualize your warmup progress and optimal send volume
5. **Fix recommendations** -- Not just what's wrong, but exactly how to fix it

### Social Proof
- "I was sending to spam for 2 weeks. InboxGuard would have caught it in 6 hours."
- "Saved me from a blacklisting that would have killed my whole outbound operation."

### CTA
Start free. Monitor 1 domain. No credit card required.

---

## Distribution Plan

| Channel | Action | Timeline |
|---------|--------|----------|
| Product Hunt | Launch day post | Week 2 |
| X/Twitter @PRINTMAXXER | Build-in-public thread | Week 1+ |
| r/coldemail | Post about domain health | Week 2 |
| r/SaaS | Launch announcement | Week 2 |
| @pipelineabuser style content | Cold email tips + tool mention | Ongoing |
| Cold email to agencies | Eat own dog food | Week 3 |
| Indie Hackers | Revenue update posts | Monthly |
| SEO | "email deliverability checker" pages | Month 2+ |
| Whop listing | Cross-sell with cold email templates | Week 2 |

---

## Build Timeline

| Day | Task |
|-----|------|
| 1 | Supabase schema + auth + domain CRUD |
| 2 | DNS health scanner (SPF/DKIM/DMARC/MX) |
| 3 | Blacklist checker (80+ DNSBLs) + alert system |
| 4 | Dashboard UI (health score, domain list, alerts) |
| 5 | Stripe integration + pricing tiers |
| 6 | Inbox placement test system |
| 7 | Landing page + launch prep |

**Total: 7 days to MVP**

---

## Revenue Projections

| Month | Free Users | Paid Users | MRR |
|-------|-----------|------------|-----|
| 1 | 200 | 15 | $500 |
| 3 | 800 | 60 | $2,200 |
| 6 | 2,000 | 200 | $7,500 |
| 12 | 5,000 | 500 | $19,000 |

---

## Competitive Landscape

| Competitor | Price | Our Edge |
|------------|-------|----------|
| Warmup Inbox | $15-$99/mo | We do monitoring, not just warmup |
| MxToolbox | Free (basic) | We add alerts + warmup + placement |
| Mail-Tester | Free (basic) | We do continuous monitoring |
| GlockApps | $79-$199/mo | We're 4x cheaper for same features |
| Mailtrap | $14-$299/mo | We focus on deliverability, not dev email testing |

**Our moat:** Cold email focus (not generic email tools), built-in recommendations from @pipelineabuser-style frameworks, integration with warmup ecosystem.

---

*Spec ready to build. Start with `npx create-next-app@latest inboxguard --typescript --tailwind --app` and add Supabase integration.*
