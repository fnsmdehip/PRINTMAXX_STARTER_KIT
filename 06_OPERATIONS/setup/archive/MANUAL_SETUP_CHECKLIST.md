# Manual Setup Checklist

Things only you can do (I can't handle payments or credentials).

---

## Already Done ✅

- [x] Stripe account (connected)
- [x] RevenueCat account (for app subscriptions)
- [x] DigitalOcean droplet (considering Hetzner switch)

---

## Day 1 Setup (Today)

### Domains
- [ ] Buy primary domain (printmaxx.com or similar)
- [ ] Buy 3-5 cold email domains (~$10 each)
  - Pattern: [brandname]-[word].com (printmaxx-hq.com, etc.)
  - Different registrars than main domain

### Hosting Decision
**DigitalOcean vs Hetzner:**

| | DigitalOcean | Hetzner |
|-|--------------|---------|
| Basic VPS | $6/mo (1GB) | $4/mo (2GB) |
| Good VPS | $12/mo (2GB) | $7/mo (4GB) |
| Location | US/EU | EU (DE/FI) |
| DDoS | Basic | Included |
| Support | Good | Good |
| Verdict | Keep if working | Switch for 40% savings |

**My take:** If your stuff works on DO, stay. If starting fresh or cost-conscious, Hetzner is better value. Don't migrate mid-project.

### Vercel (Free, 5 min)
- [ ] Connect GitHub repo
- [ ] Deploy landing site
- [ ] Connect domain

### Email Infrastructure
- [ ] Google Workspace OR Outlook for cold domains
  - Google: $6/user/mo
  - Outlook: $6/user/mo
  - Create 3 inboxes per domain minimum
- [ ] Configure DNS for each domain:
  ```
  SPF: v=spf1 include:_spf.google.com ~all
  DKIM: From Google Admin console
  DMARC: v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
  ```

### Cold Email Tool (Pick One)
- [ ] Instantly.ai ($37-97/mo) - Easiest
- [ ] Smartlead ($39/mo) - Better analytics
- [ ] Emailbison ($39/mo) - Budget
- [ ] Apollo.io ($49/mo) - Data + sending

### Warmup
- [ ] Enable built-in warmup on chosen tool
- [ ] OR add Warmbox ($19/mo) for extra
- [ ] Set warmup to run 2-3 weeks before sending

---

## Day 1 Setup (Social Accounts)

### Create Accounts (Manual)
- [ ] X/Twitter - Main brand + 3 niche accounts
- [ ] TikTok - 3 niche accounts
- [ ] Instagram - 3 niche accounts (optional)
- [ ] LinkedIn - Personal profile optimized

### Immediate Actions
- [ ] Enable 2FA on all accounts
- [ ] Save backup codes in password manager
- [ ] Complete all profile fields
- [ ] Follow 10-20 relevant accounts per niche
- [ ] Start manual engagement (no posting yet)

### Proxy Setup
- [ ] Sign up for Soax ($99 minimum ~15GB)
  - OR Decodo/Smartproxy ($75 for 5GB)
- [ ] Get residential proxy credentials
- [ ] Test with browser extension first
- [ ] Assign 1 proxy config per account

---

## Day 1 Setup (Payments)

### Stripe Products (5 min)
Since you have Stripe, create products:

```
Info Products:
- Stack Guide: $47 one-time
- Full Course: $197 one-time
- Premium Bundle: $497 one-time

Services (if offering):
- Audit: $500 one-time
- Setup Package: $1,500 one-time
- Monthly Retainer: $2,000/mo

Apps (via RevenueCat):
- Monthly: $9.99/mo
- Annual: $79.99/yr
```

### RevenueCat Setup
- [ ] Create app projects (Faith, Fitness, AI)
- [ ] Connect to App Store Connect / Google Play
- [ ] Set up subscription products
- [ ] Configure webhooks for analytics

---

## Week 1 Ongoing

### Email Warmup
- [ ] Let warmup run (don't send cold yet)
- [ ] Monitor deliverability scores
- [ ] Check inbox placement

### Social Warming
- [ ] Daily manual engagement (15-30 min per account)
- [ ] First posts Day 3-5 (text only, no links)
- [ ] Respond to any interactions
- [ ] Document what works

### Content Prep
- [ ] Review generated content batches
- [ ] Edit/approve for your voice
- [ ] Queue first week of posts
- [ ] Prep email sequences

---

## Tools I Recommend You Sign Up For

### Essential (Day 1)
| Tool | Cost | Purpose |
|------|------|---------|
| Soax or Decodo | $50-100 | Proxies for automation |
| Instantly OR Emailbison | $37-39/mo | Cold email |
| Buffer or Hypefury | $15-29/mo | Social scheduling |

### Week 2+
| Tool | Cost | Purpose |
|------|------|---------|
| Apollo.io | $49/mo | Lead data |
| Deliveron | $39/mo | Email deliverability monitoring |
| Make.com | Free tier | Automation workflows |

### Optional
| Tool | Cost | Purpose |
|------|------|---------|
| Hunter.io | $49/mo | Email finding |
| ZeroBounce | Pay per use | Email verification |
| GlockApps | $59/mo | Spam testing |

---

## Credentials to Store (1Password/Bitwarden)

After setup, save:
- [ ] All social account credentials + 2FA backups
- [ ] Email account credentials
- [ ] Stripe API keys (test + live)
- [ ] RevenueCat API keys
- [ ] Proxy credentials
- [ ] Domain registrar logins
- [ ] Hosting (DO/Hetzner) credentials
- [ ] Cold email tool credentials

---

## What I'll Do While You Set Up

Once you have accounts created, I can:
1. Generate first content batches for each niche
2. Create Playwright scripts for your proxy setup
3. Build email sequences ready to load
4. Draft social posts for warmup period
5. Set up tracking systems in LEDGER/

---

## Quick Decision Guide

**Proxy:** Soax (cheaper) or Decodo (bigger pool) - either works
**Email:** Instantly (easiest) or Emailbison (cheapest)
**Hosting:** Stay on DO unless you want to save ~$5/mo
**Social scheduler:** Hypefury for X focus, Buffer for multi-platform

---

Last updated: 2026-01-21
