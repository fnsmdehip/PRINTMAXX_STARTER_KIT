# The Vibe Coder Security Checklist

> Most vibe coders ship apps with ZERO security. Then they wonder why their app breaks at 10 users, their Supabase bill hits $500 from abuse, and their API keys end up on GitHub trending.

**Price:** $19 (Checklist) | $97 (Checklist + 1-hour audit call)

**Target buyer:** Solo devs, vibe coders, indie hackers who build with Cursor/v0/Bolt/Replit and ship fast without thinking about security.

**Positioning:** "You spent 4 hours building the app. Spend 30 minutes not getting wrecked."

---

## Product Structure

### Tier 1: The Checklist ($19)

PDF + Notion template. 47-point security checklist organized by priority. Copy-paste code snippets for every fix. Takes 30 minutes to run through.

### Tier 2: Checklist + Audit ($97)

Everything in Tier 1 + a 1-hour screen share where I run the automated audit script on your app and walk through every finding. You get a written report with exact fixes.

---

## THE CHECKLIST

### Section 1: Authentication (CRITICAL)

- [ ] **1.1** Auth library used (NextAuth, Clerk, Supabase Auth, Firebase Auth). NOT custom JWT implementation
- [ ] **1.2** Password minimum 8 characters, no max limit below 128
- [ ] **1.3** Rate limit login attempts (5 failures = 15 min lockout)
- [ ] **1.4** Email verification required before account activation
- [ ] **1.5** Password reset tokens expire in 1 hour max
- [ ] **1.6** Session tokens rotated on login/privilege change
- [ ] **1.7** Logout actually invalidates the session server-side (not just clearing cookies)
- [ ] **1.8** OAuth state parameter used to prevent CSRF
- [ ] **1.9** Multi-factor auth available for admin/sensitive actions

**Code snippet - Rate limiting login (Next.js + Upstash):**
```typescript
import { Ratelimit } from "@upstash/ratelimit";
import { Redis } from "@upstash/redis";

const ratelimit = new Ratelimit({
  redis: Redis.fromEnv(),
  limiter: Ratelimit.slidingWindow(5, "15 m"), // 5 attempts per 15 min
});

// In your login API route:
const { success } = await ratelimit.limit(ip);
if (!success) return new Response("Too many attempts", { status: 429 });
```

### Section 2: Row Level Security / Database (CRITICAL)

- [ ] **2.1** RLS enabled on EVERY Supabase table (not just some)
- [ ] **2.2** Firestore/RTDB rules are NOT `allow read, write: if true`
- [ ] **2.3** Users can only read/write their own data (test with different user tokens)
- [ ] **2.4** Admin operations require admin role check server-side
- [ ] **2.5** Database credentials are NOT in client-side code
- [ ] **2.6** No `select *` on tables with sensitive columns
- [ ] **2.7** Soft delete preferred over hard delete (audit trail)
- [ ] **2.8** Database backups configured and tested

**Test your RLS (Supabase):**
```sql
-- Run this in SQL editor to check RLS status
SELECT schemaname, tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public';
-- If rowsecurity = false on ANY table, you have a problem
```

**Fix RLS template:**
```sql
ALTER TABLE your_table ENABLE ROW LEVEL SECURITY;

-- Users can only see their own rows
CREATE POLICY "Users see own data" ON your_table
  FOR SELECT USING (auth.uid() = user_id);

-- Users can only insert their own rows
CREATE POLICY "Users insert own data" ON your_table
  FOR INSERT WITH CHECK (auth.uid() = user_id);
```

### Section 3: API Key Security (CRITICAL)

- [ ] **3.1** No secret API keys in client-side JavaScript bundles
- [ ] **3.2** All secret keys in environment variables (server-side only)
- [ ] **3.3** `.env` file in `.gitignore` (check: `git log --all -- .env`)
- [ ] **3.4** No API keys in git history (use `git-secrets` or `trufflehog`)
- [ ] **3.5** Supabase anon key restricted with RLS (not service_role key in client)
- [ ] **3.6** Stripe secret key is server-side only (publishable key is OK client-side)
- [ ] **3.7** OpenAI/Anthropic keys proxied through your backend (never client-side)
- [ ] **3.8** API keys have minimal required permissions (principle of least privilege)
- [ ] **3.9** Key rotation plan exists (rotate every 90 days or on team member departure)

**Quick check - are your keys exposed?**
```bash
# Search your built JS bundles for key patterns
grep -r "sk_live\|sk-ant\|AKIA\|sk-" .next/static/ 2>/dev/null
grep -r "sk_live\|sk-ant\|AKIA\|sk-" build/ 2>/dev/null
grep -r "sk_live\|sk-ant\|AKIA\|sk-" dist/ 2>/dev/null
# If ANY of these return results, you have exposed keys
```

**Next.js env var rules:**
```
# .env.local
# ONLY these are safe client-side (browser can see them):
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...  # OK, anon key is designed to be public

# NEVER prefix these with NEXT_PUBLIC_:
SUPABASE_SERVICE_ROLE_KEY=eyJ...      # Server-side only
OPENAI_API_KEY=sk-...                  # Server-side only
STRIPE_SECRET_KEY=sk_live_...          # Server-side only
```

### Section 4: Server-Side Validation (HIGH)

- [ ] **4.1** All form inputs validated server-side (not just client-side)
- [ ] **4.2** Zod/Yup schemas on API routes, not just on forms
- [ ] **4.3** File upload: type whitelist, size limit, virus scan
- [ ] **4.4** SQL injection protection (parameterized queries or ORM)
- [ ] **4.5** XSS protection (sanitize HTML input, escape output)
- [ ] **4.6** Request body size limits configured
- [ ] **4.7** Integer overflow/underflow checks on financial calculations
- [ ] **4.8** Email validation with actual format check (not just "contains @")

**Zod validation example (Next.js API route):**
```typescript
import { z } from "zod";

const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100),
  age: z.number().int().min(13).max(150),
});

export async function POST(request: Request) {
  const body = await request.json();
  const result = CreateUserSchema.safeParse(body);
  if (!result.success) {
    return Response.json({ error: result.error.flatten() }, { status: 400 });
  }
  // result.data is now typed and validated
}
```

### Section 5: Rate Limiting (HIGH)

- [ ] **5.1** Global rate limit on all API endpoints (e.g., 100 req/min per IP)
- [ ] **5.2** Stricter rate limit on auth endpoints (5 req/15 min)
- [ ] **5.3** Stricter rate limit on expensive operations (AI calls, file processing)
- [ ] **5.4** Rate limit by user ID (not just IP) to prevent distributed abuse
- [ ] **5.5** 429 response includes Retry-After header
- [ ] **5.6** Rate limit on signup/registration (prevent spam accounts)
- [ ] **5.7** Rate limit on password reset requests
- [ ] **5.8** WebSocket connections limited per user

**Implementation options by stack:**
```
Next.js:     @upstash/ratelimit (Redis-based, serverless-friendly)
Express:     express-rate-limit (in-memory or Redis store)
Cloudflare:  WAF rate limiting rules (edge-level, no code needed)
Vercel:      Vercel WAF (if on Pro plan) or Upstash
```

### Section 6: CAPTCHA / Bot Protection (HIGH)

- [ ] **6.1** CAPTCHA on signup form (Turnstile, hCaptcha, or reCAPTCHA v3)
- [ ] **6.2** CAPTCHA on login after 3 failed attempts
- [ ] **6.3** CAPTCHA on contact/feedback forms
- [ ] **6.4** CAPTCHA on any public-facing form that triggers server work
- [ ] **6.5** Honeypot fields on forms (hidden field that bots fill, humans dont)
- [ ] **6.6** Bot user-agent blocking on critical endpoints

**Cloudflare Turnstile (free, privacy-friendly):**
```typescript
// Client-side
<div class="cf-turnstile" data-sitekey="0x4AAA..." data-callback="onTurnstileSuccess"></div>

// Server-side verification
const verifyResponse = await fetch(
  'https://challenges.cloudflare.com/turnstile/v0/siteverify',
  {
    method: 'POST',
    body: JSON.stringify({
      secret: process.env.TURNSTILE_SECRET_KEY,
      response: token,
    }),
  }
);
const data = await verifyResponse.json();
if (!data.success) return new Response("Bot detected", { status: 403 });
```

### Section 7: CORS Configuration (MEDIUM)

- [ ] **7.1** CORS not set to wildcard `*` (especially with credentials)
- [ ] **7.2** Allowed origins explicitly listed (your domain only)
- [ ] **7.3** `Access-Control-Allow-Credentials` only with specific origins, never with `*`
- [ ] **7.4** Preflight responses cached appropriately (Access-Control-Max-Age)
- [ ] **7.5** Only necessary HTTP methods allowed (not `*`)

**Next.js API route CORS:**
```typescript
const ALLOWED_ORIGINS = [
  'https://yourdomain.com',
  'https://www.yourdomain.com',
];

export async function GET(request: Request) {
  const origin = request.headers.get('origin');
  const headers = new Headers();

  if (origin && ALLOWED_ORIGINS.includes(origin)) {
    headers.set('Access-Control-Allow-Origin', origin);
    headers.set('Access-Control-Allow-Methods', 'GET, POST');
    headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  }

  return new Response(JSON.stringify({ data: "..." }), { headers });
}
```

### Section 8: Security Headers (MEDIUM)

- [ ] **8.1** `Strict-Transport-Security` (HSTS) enabled
- [ ] **8.2** `Content-Security-Policy` configured
- [ ] **8.3** `X-Content-Type-Options: nosniff`
- [ ] **8.4** `X-Frame-Options: DENY` (or SAMEORIGIN)
- [ ] **8.5** `Referrer-Policy: strict-origin-when-cross-origin`
- [ ] **8.6** `Permissions-Policy` restricting unused browser APIs
- [ ] **8.7** Server version not disclosed in headers

**Next.js security headers (next.config.js):**
```javascript
const securityHeaders = [
  { key: 'Strict-Transport-Security', value: 'max-age=31536000; includeSubDomains' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'X-Frame-Options', value: 'DENY' },
  { key: 'X-XSS-Protection', value: '1; mode=block' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
  { key: 'Content-Security-Policy', value: "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval'; style-src 'self' 'unsafe-inline'" },
];

module.exports = {
  async headers() {
    return [{ source: '/(.*)', headers: securityHeaders }];
  },
};
```

### Section 9: Environment & Deployment (MEDIUM)

- [ ] **9.1** `.env` in `.gitignore`
- [ ] **9.2** No secrets in `docker-compose.yml` or `Dockerfile`
- [ ] **9.3** Production environment variables set through hosting dashboard (Vercel, Railway, etc.)
- [ ] **9.4** Debug mode disabled in production
- [ ] **9.5** Error pages don't show stack traces
- [ ] **9.6** Source maps disabled in production (or restricted to error tracking service)
- [ ] **9.7** `node_modules` not deployed
- [ ] **9.8** Build artifacts not exposing source code
- [ ] **9.9** HTTPS enforced (redirect HTTP to HTTPS)

### Section 10: Dependency Audit (MEDIUM)

- [ ] **10.1** `npm audit` run and critical/high vulns fixed
- [ ] **10.2** No abandoned packages (last update > 2 years)
- [ ] **10.3** Lock file committed (package-lock.json or yarn.lock)
- [ ] **10.4** Dependabot or Renovate configured for auto-updates
- [ ] **10.5** No unnecessary dependencies (bloat = attack surface)
- [ ] **10.6** License check done (no GPL in commercial projects)

**Quick audit commands:**
```bash
npm audit                        # Check for known vulns
npm audit fix                    # Auto-fix what's possible
npx depcheck                     # Find unused dependencies
npx license-checker --summary    # Check licenses
```

### Section 11: Monitoring & Incident Response (LOW)

- [ ] **11.1** Error tracking configured (Sentry, LogRocket, etc.)
- [ ] **11.2** Uptime monitoring configured (UptimeRobot, Better Stack)
- [ ] **11.3** Unusual traffic alerts (Cloudflare, Vercel analytics)
- [ ] **11.4** Database query logging for suspicious patterns
- [ ] **11.5** Incident response plan exists (even a simple checklist)
- [ ] **11.6** Contact email for security reports (security@yourdomain.com)

---

## 30-Minute Speed Run

Dont have time for all 47 points? Do these 10 in 30 minutes and you'll catch 80% of the real problems:

1. **RLS enabled on every Supabase table** (2 min - check dashboard)
2. **No secret keys in client bundles** (3 min - grep your build folder)
3. **`.env` in `.gitignore`** (1 min)
4. **Rate limiting on auth endpoints** (5 min - add Upstash)
5. **Zod validation on API routes** (5 min - add schemas)
6. **Security headers in next.config** (3 min - copy paste above)
7. **CORS restricted to your domain** (2 min)
8. **Turnstile on signup form** (5 min)
9. **`npm audit fix`** (2 min)
10. **Error pages dont show stack traces** (2 min - check production)

---

## Common Vibe Coder Mistakes (The Hall of Shame)

### 1. "I'll add security later"
You wont. And by "later" your Supabase bill is $500 because someone found your unprotected endpoint and scraped your entire database.

### 2. Supabase anon key = service role key
The anon key is designed to be public. The service role key bypasses ALL RLS. If you put the service role key in your frontend, you gave every visitor admin access to your database.

### 3. "Cursor generated it so it's probably secure"
Cursor/v0/Bolt generate functional code, not secure code. They will happily put your OpenAI key in a client-side component because you asked for "an AI chat feature."

### 4. No rate limiting on AI endpoints
Your AI feature costs $0.01 per request. Someone writes a script that hits it 100K times. Thats $1,000 on your credit card. Rate limit everything that costs you money.

### 5. Client-side authorization
```typescript
// This is NOT security
if (user.role === 'admin') {
  showAdminPanel();
}
// Anyone can open DevTools, change user.role to 'admin', and see everything
// ALWAYS check roles server-side
```

### 6. Trusting Vercel's security for everything
Vercel handles deployment security. They dont handle YOUR application security. RLS, rate limiting, input validation, API key management = all YOUR responsibility.

---

## Automated Audit Tool

Run our security audit script on your app:

```bash
# Quick scan (30 seconds)
python3 app_security_audit.py https://your-app.vercel.app

# Full scan including rate limit test (2 minutes)
python3 app_security_audit.py https://your-app.vercel.app --full

# Save report
python3 app_security_audit.py https://your-app.vercel.app --output report.json
```

The script checks: security headers, CORS, API key exposure, sensitive file exposure, cookie security, SSL/TLS, and Supabase/Firebase misconfigurations.

---

## Gumroad Listing Copy

**Title:** The Vibe Coder Security Checklist - Stop Shipping Insecure Apps

**Tagline:** 47-point security checklist for indie hackers who build with Cursor, v0, Bolt, and Replit. 30 minutes to not get wrecked.

**Description:**

You spent 4 hours building the app. Spend 30 minutes not getting wrecked.

Most vibe coders ship apps with zero security. No rate limiting. No RLS. API keys in the client bundle. Then they wonder why:

- Their Supabase bill hit $500 from endpoint abuse
- Someone scraped their entire user database
- Their OpenAI key got leaked and racked up $2K in charges

This checklist covers everything:

- Authentication hardening (9 checks)
- Row Level Security / Database (8 checks)
- API Key Security (9 checks)
- Server-Side Validation (8 checks)
- Rate Limiting (8 checks)
- CAPTCHA / Bot Protection (6 checks)
- CORS Configuration (5 checks)
- Security Headers (7 checks)
- Environment & Deployment (9 checks)
- Dependency Audit (6 checks)
- Monitoring & Incident Response (6 checks)

Plus: copy-paste code snippets for every fix, a 30-minute speed run for the impatient, and an automated audit script you can run on any URL.

$19 gets you the checklist. $97 gets you the checklist + a 1-hour screen share where I run the audit on YOUR app and walk through every finding.

**Tags:** security, vibe-coding, indie-hacker, nextjs, supabase, checklist

---

## Upsell: Security Audit Service ($497+)

For apps with real users/revenue:

- Full automated + manual audit
- Written report with severity ratings
- Code-level fix recommendations
- 30-minute follow-up call after fixes
- Re-audit to verify fixes

Position as: "The insurance policy for your $10K MRR app."

Target: indie hackers at $1K-10K MRR who can't afford a full pentest but need basic security.
