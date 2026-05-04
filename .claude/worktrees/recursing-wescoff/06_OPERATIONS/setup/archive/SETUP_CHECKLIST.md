# PRINTMAXX Services & Stack Setup Checklist

**Last Updated:** 2026-01-20
**Purpose:** Complete checklist for setting up all services needed to run the PrintMaxx system

---

## Phase 1: Foundation (Week 1) - $55-60

### Browser Automation (Required for Alpha Scraping)
- [ ] **Brave Browser** - Free
  - Download: https://brave.com/download/
  - Enable: Settings > Extensions > "Allow extensions to execute JavaScript on pages"
  - Why: AppleScript automation for tweet/content extraction

### Proxy & Verification (Required for Account Creation)
- [ ] **Decodo Proxies** - $50/mo
  - URL: https://app.decodo.com
  - Plan: Starter (5GB residential)
  - Why: Clean IPs for social account creation/warmup
  - Setup: Get API key, configure in GoLogin

- [ ] **SMSPool** - $5-10 one-time
  - URL: https://smspool.net
  - Why: Phone verification for social accounts
  - Setup: Add $5-10 balance, use US numbers

- [ ] **GoLogin** - Free tier
  - URL: https://gologin.com
  - Why: Browser fingerprint management for multiple accounts
  - Setup: Create profiles for each niche account

### Email Setup (Required)
- [ ] **ProtonMail** - Free
  - Create accounts:
    - printmaxxer@protonmail.com (main)
    - ai.workflows.tips@protonmail.com (AI niche)
    - daily.anchor.faith@protonmail.com (Faith niche)
    - three.hour.physique@protonmail.com (Fitness niche)
  - Why: Social account registration, newsletter sending

---

## Phase 2: Content & Automation (Week 1-2) - $0-200

### AI/LLM Tools
- [ ] **Claude Max** - $200/mo (already have)
  - Why: Code, content generation, agent runs
  - Verify: API access enabled

- [ ] **Cursor Pro** - $20/mo (optional)
  - URL: https://cursor.so
  - Why: AI-powered code editing
  - Alternative: VS Code with Claude extension

### Content Tools
- [ ] **Canva** - Free tier
  - URL: https://canva.com
  - Why: Social graphics, thumbnails
  - Setup: Create brand kit with PrintMaxx colors

- [ ] **CapCut** - Free
  - URL: https://capcut.com
  - Why: Video editing for TikTok/Reels
  - Setup: Download desktop app

### Development
- [ ] **Node.js 18+** - Free
  - Verify: `node --version`
  - Why: Next.js site

- [ ] **Python 3.11+** - Free
  - Verify: `python3 --version`
  - Why: Automation scripts

- [ ] **Homebrew** - Free (Mac)
  - Verify: `brew --version`
  - Install: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

---

## Phase 3: Social Accounts (Week 1) - $0

### X/Twitter
- [ ] @PRINTMAXXER (main account)
- [ ] AI niche account (ai_workflows_tips)
- [ ] Faith niche account (dailyanchor_faith)
- [ ] Fitness niche account (3hourphysique)

### TikTok
- [ ] AI niche account
- [ ] Faith niche account
- [ ] Fitness niche account

### Instagram
- [ ] AI niche account
- [ ] Faith niche account
- [ ] Fitness niche account

### YouTube (Optional, Week 2+)
- [ ] AI niche channel
- [ ] Faith niche channel
- [ ] Fitness niche channel

---

## Phase 4: Cold Email Infrastructure (Week 5+) - $80-150/mo

### Lane A: API Platforms
- [ ] **Instantly** - $37/mo
  - URL: https://instantly.ai
  - Why: Warm email sending at scale
  - Setup: Connect domains, set sending limits

- [ ] **Smartlead** - $39/mo (alternative)
  - URL: https://smartlead.ai
  - Why: Backup sender, A/B testing

### Lane B: Inbox-as-Service
- [ ] **DeliverOn** - $20-40/mo
  - URL: https://deliveron.com
  - Why: Pre-warmed inboxes
  - Setup: Order 5-10 inboxes

### Lane C: DIY Domains
- [ ] **Namecheap** - $10-15/domain/year
  - URL: https://namecheap.com
  - Buy: 3-5 similar domains per niche
  - Setup: Configure MX records

- [ ] **Google Workspace** - $6/mo/inbox
  - URL: https://workspace.google.com
  - Why: Highest deliverability
  - Setup: Connect to sending platform

### Lane D: Gmail Method (VIP Targets)
- [ ] Manual Gmail accounts
  - Why: Highest deliverability for key prospects
  - Setup: Use for <10 sends/day

---

## Phase 5: Product & Payment (Week 2+) - Variable

### Digital Product Hosting
- [ ] **Gumroad** - Free (5% + fees on sales)
  - URL: https://gumroad.com
  - Why: Easiest setup, handles payments
  - Setup: Create products from PRODUCTS/gumroad_copy/

- [ ] **Notion** - Free
  - URL: https://notion.so
  - Why: AI Clarity Stack product delivery
  - Setup: Create template, enable duplication

### Payment Processing
- [ ] **Stripe** - 2.9% + $0.30/transaction
  - URL: https://stripe.com
  - Why: Direct payment processing (higher margin than Gumroad)
  - Setup: Connect to landing page

---

## Phase 6: Analytics & Tracking (Week 2+) - $0

### Website Analytics
- [ ] **Plausible** - Free self-host / $9/mo cloud
  - URL: https://plausible.io
  - Why: Privacy-friendly, GDPR compliant
  - Alternative: Google Analytics (free, less private)

### Social Analytics
- [ ] **Built-in platform analytics** - Free
  - X: Analytics dashboard
  - TikTok: Creator tools
  - IG: Insights

### Email Analytics
- [ ] **Sending platform dashboards** - Included
  - Track: Open rates, reply rates, bounce rates

---

## Phase 7: Automation Tools (Optional) - $0-50/mo

### Workflow Automation
- [ ] **n8n** - Free self-host / $20/mo cloud
  - URL: https://n8n.io
  - Why: Connect tools, automate workflows
  - Alternative: Make.com, Zapier

### Scheduling
- [ ] **Buffer** - Free tier (3 channels)
  - URL: https://buffer.com
  - Why: Schedule social posts
  - Alternative: Manual posting

---

## Quick Start Commands

### Verify Development Environment
```bash
# Check Node.js
node --version  # Should be 18+

# Check Python
python3 --version  # Should be 3.11+

# Check npm
npm --version

# Install project dependencies
cd LANDING/printmaxx-site && npm install
```

### Run Local Development
```bash
# Start Next.js dev server
cd LANDING/printmaxx-site && npm run dev

# Test build
cd LANDING/printmaxx-site && npm run build
```

### Test Alpha Extractor
```bash
# Dry run to verify setup
python3 AUTOMATIONS/daily_alpha_extractor.py --dry-run

# Run X accounts only
python3 AUTOMATIONS/daily_alpha_extractor.py --platform X --max 3
```

---

## Cost Summary by Phase

| Phase | Timeline | Cost |
|-------|----------|------|
| Foundation | Week 1 | $55-60 |
| Content & Automation | Week 1-2 | $0-200 |
| Social Accounts | Week 1 | $0 |
| Cold Email | Week 5+ | $80-150/mo |
| Product & Payment | Week 2+ | Variable (% of sales) |
| Analytics | Week 2+ | $0-9/mo |
| Automation | Optional | $0-50/mo |

**Total Week 1:** $55-260
**Total Monthly (after Week 5):** $135-409/mo + sales %

---

## Priority Order

1. **Day 1:** Brave, Python, Node.js (dev environment)
2. **Day 1-2:** ProtonMail accounts, Decodo, SMSPool, GoLogin
3. **Day 2-7:** Social account creation and warmup
4. **Week 2:** Gumroad products, Canva brand kit
5. **Week 3-4:** Analytics, content scheduling
6. **Week 5+:** Cold email infrastructure

---

## Verification Checklist

Run through this before starting any major operation:

```
[ ] Brave browser open with JS execution enabled
[ ] Logged into X on Brave (for alpha scraping)
[ ] Python 3.11+ installed
[ ] Node.js 18+ installed
[ ] Project dependencies installed (npm install)
[ ] LEDGER/*.csv files readable
[ ] AUTOMATIONS/*.py scripts executable
```
