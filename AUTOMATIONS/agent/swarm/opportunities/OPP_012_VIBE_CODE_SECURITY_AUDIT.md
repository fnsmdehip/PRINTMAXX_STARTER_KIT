# OPP_012: AI Security Audit for Vibe-Coded Apps

**Score: 9.0/10** | Fit: 10 | Effort: 2 | ROI: 9
**Created:** 2026-03-07 | **Source:** swarm_opportunity_scanner
**Status:** PENDING_REVIEW

---

## What

Automated security audit service for apps built with AI/vibe-coding tools (Cursor, v0, Bolt, Lovable, Replit Agent). Charge $299-$499 per audit. Use Python + Playwright + Claude to scan for OWASP Top 10, exposed secrets, broken auth, XSS, SQL injection, and misconfigurations. Deliver a branded PDF report with severity ratings and fix instructions.

## Why

- **Massive validated demand.** r/SaaS thread about vibe-coding security gaps got 76 comments. HN thread about AI-generated code vulnerabilities hit 929 points.
- **$0 startup cost.** Python scripts + Claude API (pennies per audit) + Playwright for dynamic testing.
- **Vibe-coding explosion.** Millions of non-technical founders shipping apps with Cursor/Bolt/Lovable. Most have ZERO security review.
- **Fear sells.** "Your vibe-coded app has 14 critical vulnerabilities" is a consequence-first hook that converts.
- **Recurring potential.** Monthly monitoring subscription after initial audit ($99/mo).
- **Content machine.** Every audit finding = tweet content. "I audited 50 vibe-coded apps. 47 had hardcoded API keys."

## How

### Audit Pipeline Architecture
```
Client submits URL → Playwright crawls all routes →
Python static analysis (if repo access) →
Claude API analyzes code patterns →
OWASP checklist automated scan →
Generate severity-scored PDF report →
Deliver via email with fix recommendations
```

### Automated Checks (build as Python scripts)
1. **Exposed secrets scan** — grep .env files, API keys in client-side JS, hardcoded credentials
2. **Auth testing** — broken access control, session management, JWT validation
3. **XSS detection** — inject test payloads via Playwright, check for reflection
4. **SQL injection probes** — parameterized query validation
5. **CORS misconfiguration** — check Access-Control headers
6. **Dependency audit** — npm audit / pip audit via API
7. **SSL/TLS check** — certificate validity, HSTS headers
8. **Rate limiting test** — hammer endpoints, check for throttling
9. **Error disclosure** — trigger errors, check for stack traces
10. **Client-side secrets** — scan JS bundles for API keys, tokens

### First 3 Steps (This Week)

1. **Build core audit script** (1 day)
   - Python script that takes a URL, crawls with Playwright, runs all 10 checks
   - Output: JSON with findings, severity (CRITICAL/HIGH/MEDIUM/LOW/INFO)
   - Use existing Playwright infrastructure from our scraper stack

2. **Build PDF report generator** (half day)
   - Branded template with logo, severity badges, fix recommendations
   - Use reportlab or weasyprint (Python PDF libs)
   - Include executive summary + detailed findings + remediation steps

3. **Create landing page + cold outreach list** (half day)
   - Landing page on surge.sh: "Is your vibe-coded app secure?"
   - Scrape r/SaaS, r/indiehackers, Twitter for people who mention Cursor/Bolt/Lovable
   - Cold DM: "I scanned your app's public surface. Found 3 issues. Want the full report?"

### Pricing
| Tier | Price | Includes |
|------|-------|----------|
| Quick Scan | $99 | External-only automated scan, 1-page summary |
| Full Audit | $299 | Deep scan + code review (if repo access) + PDF report |
| Premium | $499 | Full audit + 30-min walkthrough call + 30-day re-scan |
| Monthly Monitor | $99/mo | Weekly automated scans + alerts |

## Expected ROI

| Metric | Value |
|--------|-------|
| Startup cost | $0 (Python + Claude API pennies) |
| Time to first revenue | 1 week |
| Monthly potential (3mo) | $1,500-3,000/mo (5-10 audits) |
| Monthly potential (6mo) | $5,000-10,000/mo (scale + monitoring subs) |
| Competition | Low (nobody targets vibe-coded apps specifically) |
| Stack fit | Perfect (Python + Playwright + Claude) |
| Recurring | Yes (monthly monitoring tier) |

## Risk Assessment
- Legal: must clarify "authorized testing only" — client must own the app
- Liability: report disclaimers, no guarantees
- Quality: automated scans miss things — position as "first pass" not "penetration test"
- Scale: manual review bottleneck at $499 tier — automate more over time

## Content Generation (Zero Waste)
- "I audited 50 vibe-coded apps built with Cursor. here's what I found." (thread)
- "your Bolt app has hardcoded Stripe keys in the client bundle. I checked." (reply bait)
- "the vibe coding security gap is a $10M opportunity nobody's building for" (hot take)
- Case studies from each audit (anonymized) = endless content
