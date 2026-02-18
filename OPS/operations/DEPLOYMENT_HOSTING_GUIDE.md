# Deployment and Hosting Guide

**Purpose:** Comprehensive guide for deploying PRINTMAXX web properties on Vercel and alternatives.

**Last Updated:** 2026-01-25

---

## Quick Start (Vercel)

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to production
cd LANDING/printmaxx-site
vercel --prod

# Deploy preview
vercel
```

---

## Table of Contents

1. [Vercel Setup](#vercel-setup)
2. [Deployment Workflow](#deployment-workflow)
3. [Environment Variables](#environment-variables)
4. [Custom Domains](#custom-domains)
5. [Vercel Features](#vercel-features)
6. [Cost Optimization](#cost-optimization)
7. [Alternatives Comparison](#alternatives-comparison)
8. [PRINTMAXX-Specific Configuration](#printmaxx-specific-configuration)

---

## Vercel Setup

### Initial Project Setup

1. **Create Vercel Account**
   - Go to vercel.com/signup
   - Use GitHub login (recommended for Git integration)
   - Select Hobby (free) or Pro ($20/mo) plan

2. **Import Repository**
   ```bash
   # Option 1: Import via dashboard
   # vercel.com/new → Import Git Repository

   # Option 2: CLI deployment
   cd LANDING/printmaxx-site
   vercel
   ```

3. **Configure Project Settings**
   - Framework Preset: Next.js (auto-detected)
   - Root Directory: `LANDING/printmaxx-site`
   - Build Command: `npm run build` (default)
   - Output Directory: `.next` (default)
   - Install Command: `npm install` (default)

### Project Structure for Vercel

```
LANDING/printmaxx-site/
├── app/                    # Next.js App Router
│   ├── page.tsx           # Homepage
│   ├── truth/[slug]/      # Dynamic truth pages
│   ├── magnet/            # Lead magnets
│   └── api/               # API routes (Vercel Functions)
├── public/                # Static assets (served via CDN)
├── .env.local            # Local env vars (git-ignored)
├── .env.example          # Template for required vars
├── next.config.ts        # Next.js configuration
└── vercel.json           # Vercel-specific config (optional)
```

---

## Deployment Workflow

### Git-Based Deployments (Recommended)

**Automatic deployments on push:**

| Branch | Environment | URL Pattern |
|--------|-------------|-------------|
| `main` | Production | yourdomain.com |
| `feature/*` | Preview | feature-*.vercel.app |
| PR branches | Preview | pr-123-*.vercel.app |

**Setup:**
1. Connect GitHub repo to Vercel project
2. Configure production branch (default: `main`)
3. Push commits to trigger deployments

### CLI Deployments

```bash
# Preview deployment (staging)
vercel

# Production deployment
vercel --prod

# Deploy specific directory
vercel LANDING/printmaxx-site --prod

# Deploy with build output
vercel build
vercel deploy --prebuilt
```

### Deploy Hooks (Webhooks)

Create a deploy hook for external triggers:

1. Project Settings → Git → Deploy Hooks
2. Create hook with branch name
3. Use the URL to trigger deployments:

```bash
# Trigger via curl
curl -X POST https://api.vercel.com/v1/integrations/deploy/...

# Use in GitHub Actions, cron jobs, etc.
```

### Rollbacks

```bash
# Via CLI
vercel rollback

# Via dashboard
# Deployments → Select deployment → Promote to Production
```

---

## Environment Variables

### Configuration Levels

| Level | Scope | Use Case |
|-------|-------|----------|
| Project | All deployments | API keys, database URLs |
| Team | All team projects | Shared services |
| Environment | Production/Preview/Dev | Environment-specific values |
| Branch | Specific branches | Feature flags, testing |

### Setting Environment Variables

**Dashboard:**
1. Project Settings → Environment Variables
2. Add key-value pair
3. Select environments (Production, Preview, Development)

**CLI:**
```bash
# Add variable
vercel env add VARIABLE_NAME

# Pull to local
vercel env pull .env.local

# List variables
vercel env ls
```

### PRINTMAXX Required Variables

```env
# API Keys
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...

# Database (if using)
DATABASE_URL=postgres://...

# Analytics
NEXT_PUBLIC_GA_ID=G-...

# Lead Capture
SMTP_HOST=...
SMTP_USER=...
SMTP_PASS=...

# RevenueCat (for apps)
REVENUECAT_API_KEY=...

# Feature Flags
NEXT_PUBLIC_ENABLE_BETA=false
```

### Environment-Specific Variables

```bash
# Production only
NEXT_PUBLIC_API_URL=https://api.printmaxx.com

# Preview only
NEXT_PUBLIC_API_URL=https://staging-api.printmaxx.com

# Development only
NEXT_PUBLIC_API_URL=http://localhost:3001
```

### Security Best Practices

1. **Never commit secrets to git**
   - Use `.env.local` for local development
   - Add `.env*` to `.gitignore`

2. **Use NEXT_PUBLIC_ prefix carefully**
   - Variables with `NEXT_PUBLIC_` are exposed to browser
   - Keep API keys server-side only

3. **Rotate credentials regularly**
   - Update in Vercel dashboard
   - Redeploy to apply changes

---

## Custom Domains

### Adding a Domain

**Dashboard:**
1. Project Settings → Domains
2. Add domain (e.g., `printmaxx.com`)
3. Follow DNS configuration instructions

**CLI:**
```bash
vercel domains add printmaxx.com
```

### DNS Configuration Options

**Option 1: Vercel Nameservers (Recommended)**
- Full DNS management on Vercel
- Automatic SSL
- Edge network optimization

```
Nameservers:
ns1.vercel-dns.com
ns2.vercel-dns.com
```

**Option 2: External DNS (A Record)**
```
Type: A
Name: @
Value: 76.76.21.21
```

**Option 3: CNAME (Subdomains)**
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

### Multi-Domain Setup for PRINTMAXX

| Domain | Use | Project |
|--------|-----|---------|
| printmaxx.com | Main landing | printmaxx-site |
| prayerlock.app | PrayerLock landing | prayerlock-landing |
| walktounlock.com | WalkToUnlock landing | walktounlock-landing |
| stackgenerator.com | Lead magnet | printmaxx-site |

### SSL Certificates

- **Automatic:** Vercel provisions SSL certificates automatically
- **Renewal:** Certificates auto-renew before expiration
- **Custom:** Enterprise plans support custom certificates

### Redirect Configuration

Add to `vercel.json`:
```json
{
  "redirects": [
    {
      "source": "/old-page",
      "destination": "/new-page",
      "permanent": true
    }
  ]
}
```

Or use Next.js config:
```typescript
// next.config.ts
export default {
  async redirects() {
    return [
      {
        source: '/old-page',
        destination: '/new-page',
        permanent: true,
      },
    ]
  },
}
```

---

## Vercel Features

### CDN and Edge Network

**Global Distribution:**
- 126 Points of Presence (PoPs) worldwide
- 20 compute-capable regions
- Automatic routing to nearest edge

**Caching:**
```typescript
// API route with caching
export async function GET() {
  return new Response(data, {
    headers: {
      'Cache-Control': 's-maxage=3600, stale-while-revalidate=86400',
    },
  })
}
```

**Cache Control Headers:**
| Header | Effect |
|--------|--------|
| `s-maxage=N` | Cache for N seconds on CDN |
| `stale-while-revalidate` | Serve stale while revalidating |
| `no-store` | Never cache |

### Vercel Functions (Serverless)

**Creating a Function:**
```typescript
// app/api/leads/route.ts
export async function POST(request: Request) {
  const data = await request.json()
  // Process lead
  return Response.json({ success: true })
}
```

**Configuration:**
```typescript
export const config = {
  runtime: 'nodejs', // or 'edge'
  regions: ['iad1'], // Washington DC (default)
  maxDuration: 30, // seconds (Pro: 60, Enterprise: 900)
}
```

**Regions:**
| Region | Code | Best For |
|--------|------|----------|
| Washington DC | iad1 | US East, default |
| San Francisco | sfo1 | US West |
| Frankfurt | fra1 | Europe |
| Singapore | sin1 | Asia Pacific |

### Edge Functions

**When to Use:**
- Ultra-low latency (runs at edge PoPs)
- Simple logic (A/B testing, redirects, auth)
- Limited to Edge runtime APIs

```typescript
// middleware.ts
export const config = {
  matcher: '/api/:path*',
}

export function middleware(request: Request) {
  // Runs at the edge
}
```

### Vercel Storage

**Blob Storage (Files):**
```typescript
import { put } from '@vercel/blob'

const blob = await put('images/avatar.png', file, {
  access: 'public',
})
```

**Edge Config (Key-Value):**
```typescript
import { get } from '@vercel/edge-config'

const featureFlag = await get('enable_beta')
```

**Marketplace Databases:**
- Neon (Postgres)
- Upstash (Redis/KV)
- Supabase
- PlanetScale

### Analytics

**Web Analytics:**
- Page views, visitors, bounce rate
- Top pages, referrers
- Demographics (country, browser, device)
- Privacy-focused (no cookies)

**Speed Insights:**
- Core Web Vitals (LCP, FID, CLS)
- Real user monitoring
- Performance trends

**Setup:**
```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react'
import { SpeedInsights } from '@vercel/speed-insights/next'

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  )
}
```

---

## Cost Optimization

### Pricing Tiers

| Plan | Cost | Best For |
|------|------|----------|
| Hobby | Free | Personal projects, testing |
| Pro | $20/mo | Small teams, production sites |
| Enterprise | Custom | Large scale, support SLA |

### Hobby Plan Limits

| Resource | Limit |
|----------|-------|
| Deployments | 100/day |
| Serverless Function Execution | 100 GB-Hours |
| Edge Function Execution | 500K invocations |
| Bandwidth | 100 GB |
| Build Execution | 100 Hours |
| Concurrent Builds | 1 |
| Team Members | 1 |

### Pro Plan Included

| Resource | Included | Overage |
|----------|----------|---------|
| Deployments | Unlimited | - |
| Serverless Execution | 1000 GB-Hours | $0.18/GB-Hour |
| Edge Execution | 1M invocations | $0.65/M |
| Bandwidth | 1 TB | $0.15/GB |
| Build Execution | 400 Hours | $0.03/min |

### Cost Reduction Strategies

**1. Optimize Caching**
```typescript
// Cache API responses
export async function GET() {
  return new Response(data, {
    headers: {
      'Cache-Control': 's-maxage=86400', // 24 hours
    },
  })
}
```

**2. Use Static Generation**
```typescript
// Static pages = no function execution
export const dynamic = 'force-static'
```

**3. Incremental Static Regeneration (ISR)**
```typescript
// Regenerate every hour
export const revalidate = 3600
```

**4. Edge Functions for Simple Logic**
```typescript
// Edge is cheaper than Serverless for simple tasks
export const runtime = 'edge'
```

**5. Optimize Images**
```typescript
// Use Next.js Image (auto-optimized)
import Image from 'next/image'
<Image src="/hero.jpg" width={1200} height={600} />
```

**6. Monitor Usage**
- Dashboard → Usage tab
- Set up usage alerts
- Review monthly breakdown

### PRINTMAXX Cost Estimate

| Component | Monthly Usage | Cost (Pro) |
|-----------|---------------|------------|
| Main landing | ~10K visits | Included |
| API routes (leads) | ~1K calls | Included |
| Truth pages (static) | ~5K visits | Included |
| Images (CDN) | ~50 GB | Included |
| **Total** | - | **$20/mo** |

---

## Alternatives Comparison

### Netlify

| Feature | Vercel | Netlify |
|---------|--------|---------|
| Next.js Support | Native (creators) | Good |
| Build Speed | Fast | Fast |
| Edge Functions | Yes | Yes |
| Forms | Via API | Built-in |
| Pricing (Pro) | $20/mo | $19/mo |
| Free Tier | 100 GB bandwidth | 100 GB bandwidth |

**Best for:** JAMstack sites, simpler builds

### Cloudflare Pages

| Feature | Vercel | Cloudflare Pages |
|---------|--------|------------------|
| CDN Speed | Excellent | Excellent |
| Workers | Edge Functions | Workers (more flexible) |
| Pricing | $20/mo Pro | Free (generous) |
| Database | Marketplace | D1, KV, R2 built-in |
| Next.js Support | Native | Via adapter |

**Best for:** Edge-heavy apps, cost-sensitive projects

### Railway

| Feature | Vercel | Railway |
|---------|--------|---------|
| Focus | Frontend | Full-stack |
| Databases | Marketplace | Built-in |
| Docker | No | Yes |
| Pricing | $20/mo | $5/mo + usage |

**Best for:** Full-stack apps needing custom infrastructure

### Render

| Feature | Vercel | Render |
|---------|--------|--------|
| Static Sites | Yes | Yes (free) |
| Servers | Functions only | Full servers |
| Databases | Marketplace | Built-in Postgres |
| Background Jobs | No | Yes |

**Best for:** Apps needing persistent servers

### Recommendation for PRINTMAXX

**Use Vercel for:**
- Main landing site (printmaxx-site)
- App landing pages
- Lead magnets
- API routes (lead capture, webhooks)

**Consider alternatives for:**
- Heavy backend processing (Railway)
- Persistent databases (Supabase, PlanetScale)
- Media storage (Cloudflare R2, S3)

---

## PRINTMAXX-Specific Configuration

### vercel.json Configuration

Create `LANDING/printmaxx-site/vercel.json`:

```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["iad1"],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ],
  "redirects": [
    {
      "source": "/truth",
      "destination": "/truth/solopreneur-distribution",
      "permanent": false
    }
  ],
  "rewrites": [
    {
      "source": "/api/lead",
      "destination": "/api/leads"
    }
  ]
}
```

### API Routes for PRINTMAXX

**Lead Capture Endpoint:**
```typescript
// app/api/leads/route.ts
import { appendFile } from 'fs/promises'
import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  const { email, source } = await request.json()

  // Validate
  if (!email || !email.includes('@')) {
    return NextResponse.json({ error: 'Invalid email' }, { status: 400 })
  }

  // Log to CSV (or database)
  const timestamp = new Date().toISOString()
  const line = `${timestamp},${email},${source}\n`

  // In production, use database or external service
  // await appendFile('LEDGER/leads.csv', line)

  return NextResponse.json({ success: true })
}
```

**Webhook Endpoint:**
```typescript
// app/api/webhooks/stripe/route.ts
export async function POST(request: Request) {
  const payload = await request.text()
  const sig = request.headers.get('stripe-signature')

  // Verify webhook signature
  // Process payment events

  return new Response('OK', { status: 200 })
}
```

### Deployment Checklist

**Pre-Deployment:**
- [ ] Environment variables set in Vercel
- [ ] Build passes locally (`npm run build`)
- [ ] No TypeScript errors
- [ ] Images optimized
- [ ] API routes tested

**Post-Deployment:**
- [ ] Verify production URL works
- [ ] Test all critical paths
- [ ] Check Core Web Vitals
- [ ] Verify lead capture works
- [ ] Set up monitoring alerts

### Monitoring Setup

**Vercel Integrations:**
1. Dashboard → Integrations
2. Add: Sentry (errors), LogDNA (logs), Datadog (metrics)

**Alerts:**
1. Project Settings → Notifications
2. Configure: Deploy failures, usage alerts

---

## Troubleshooting

### Common Issues

**Build Failures:**
```bash
# Check build logs
vercel logs

# Run build locally
npm run build
```

**Function Timeouts:**
- Default: 10s (Hobby), 60s (Pro)
- Increase in vercel.json or function config

**Environment Variables Not Working:**
- Redeploy after adding vars
- Check correct environment selected
- Use `NEXT_PUBLIC_` for client-side vars

**Domain Not Connecting:**
- Verify DNS propagation (24-48 hours)
- Check A record or CNAME correct
- Try clearing DNS cache

### Support Resources

- Vercel Docs: vercel.com/docs
- Vercel Status: vercel-status.com
- Community: github.com/vercel/next.js/discussions

---

## Quick Reference

```bash
# Install CLI
npm i -g vercel

# Deploy preview
vercel

# Deploy production
vercel --prod

# Pull env vars
vercel env pull

# View logs
vercel logs

# Add domain
vercel domains add yourdomain.com

# Rollback
vercel rollback

# Check usage
vercel usage
```

---

*This guide covers Vercel deployment for PRINTMAXX. For app deployment (iOS/Android), see `MONEY_METHODS/APP_FACTORY/APP_STORE_SUBMISSION_GUIDE.md`.*
