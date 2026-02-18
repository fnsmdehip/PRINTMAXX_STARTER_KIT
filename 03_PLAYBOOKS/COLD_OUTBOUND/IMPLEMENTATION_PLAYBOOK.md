# COLD_OUTBOUND Implementation Playbook

**Method ID:** MM007
**ROI Rank:** #2 (Score: 91/100)
**Revenue model:** Per-lead fees, retainer, affiliate commissions
**Time investment:** 5-10 hrs/week ongoing, 15-20 hrs setup
**Capital required:** $30-100/mo (domains + inboxes + tools)
**Difficulty:** 5/10
**Platform risk:** 3/10 (email is decentralized, no single gatekeeper)
**Monthly potential:** $1,000-10,000
**First dollar timeline:** 2-4 weeks from first send

---

## Overview

Send cold emails and LinkedIn messages to acquire customers, promote apps, sign affiliate partners, and sell services. Uses @pipelineabuser's 6-questions framework (what you do, who for, how, problem solved, proof, ROI) in every email. Infrastructure is multi-domain, multi-inbox with proper DNS authentication to maintain deliverability in 2026's strict environment.

Proof: @caiden_cole closed $24K/mo from cold email alone. @pipelineabuser's students consistently hit $5-10K/mo within 90 days. PRINTMAXX already has 4 battle-tested sequences ready.

---

## Prerequisites

### Accounts needed
- [ ] Porkbun or Cloudflare for domains ($9-12/yr each)
- [ ] Google Workspace OR Microsoft 365 for inboxes ($6-12/user/mo)
- [ ] Instantly.ai or Smartlead ($30-97/mo) - sending platform
- [ ] Apollo.io (free tier, 100 leads/mo) or Clay ($149/mo at scale) - lead sourcing
- [ ] LinkedIn Sales Navigator ($99/mo, optional - start free)

### Tools/software
- [ ] Email warmup tool (built into Instantly/Smartlead)
- [ ] SPF/DKIM/DMARC configured on all domains
- [ ] Tracking domain set up for link tracking
- [ ] Chrome extension for LinkedIn (Apollo or similar)

### Existing assets to use
- `EMAIL_SEQUENCES.md` - 4 battle-tested sequences with templates
- `LINKEDIN_TEMPLATES.md` - 15 connection requests, voice note scripts
- `COLD_EMAIL_INFRASTRUCTURE_GUIDE.md` - Full DNS + inbox setup
- `AI_PERSONALIZATION_STACK_2026.md` - AI-powered personalization
- `COLD_DM_TEMPLATES_ALL_NICHES.md` - DM templates for all niches
- `infrastructure/EMAIL_TOOLS_COMPARISON.md` - Tool comparison
- `lead_lists/` - Lead list templates and sources
- `va_scripts/` - VA training scripts for outreach

---

## Step-by-step implementation

### Day 1: Domain + inbox setup (3-4 hours)

**Task 1: Buy cold email domains**

Buy 3-5 domains that look professional and relate to your brand. Never use your main domain for cold email.

Domain naming pattern:
```
Main domain:        printmaxx.com (NEVER use for cold)
Cold email domains: getprintmaxx.com
                    printmaxxhq.com
                    tryprintmaxx.io
                    withprintmaxx.co
```

Buy from Porkbun ($9-12/yr each): porkbun.com/products/domains

**Task 2: Set up Google Workspace inboxes**

Create 2-3 inboxes per domain:
```
Domain: getprintmaxx.com
├── alex@getprintmaxx.com
├── jordan@getprintmaxx.com
└── team@getprintmaxx.com (optional catch-all)
```

Google Workspace: workspace.google.com ($6/user/mo)
Total for 6 inboxes across 2 domains: $36/mo

**Task 3: Configure DNS authentication**

For EACH domain, add these DNS records:

SPF record (TXT):
```
v=spf1 include:_spf.google.com ~all
```

DKIM: Generated in Google Workspace Admin > Apps > Gmail > Authenticate email

DMARC record (TXT, _dmarc.yourdomain.com):
```
v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```

Verification: Use mail-tester.com (send test email, score should be 9+/10)

Full DNS walkthrough: `COLD_EMAIL_INFRASTRUCTURE_GUIDE.md` Part 1-2

**Task 4: Connect to sending platform**

Sign up for Instantly.ai ($30/mo Growth plan):
1. Add all inboxes via IMAP/SMTP or OAuth
2. Enable warmup on ALL inboxes immediately
3. Set daily sending limit: 30/inbox/day
4. Set warmup volume: ramp from 5 to 40 over 14 days

### Day 2-14: Warmup period (monitor only, 30 min/day)

**Task 5: Let inboxes warm up**

DO NOT send cold emails yet. Warmup takes 14-21 days minimum.

Daily check (5 min):
- Log into Instantly dashboard
- Verify warmup emails are flowing
- Check inbox health score (target: 90+)
- Monitor for any bounces or blocks

Timeline:
```
Days 1-7:    Warmup only. 5-15 emails/day auto.
Days 8-14:   Warmup continues. 15-30 emails/day auto.
Day 14:      Health check. If score 90+, start light sends.
Days 15-21:  Light cold sends (10-20/day per inbox) + warmup continues.
Day 21+:     Full volume (30-50/day per inbox) + warmup always on.
```

Reference safe limits: `COLD_EMAIL_INFRASTRUCTURE_GUIDE.md` Domain Age table

**Task 6: Build lead lists while warming up**

Use warmup time productively. Build 500+ targeted leads.

Lead sources (free to start):
- Apollo.io: 100 free leads/mo, filters by title/company/industry
- LinkedIn search: Manual but free, export via Chrome extension
- Google Maps: Local businesses, scrape with tools
- Industry directories: Niche-specific (e.g., Clutch for agencies)

Lead list format (CSV):
```
first_name,last_name,email,company,title,industry,personalization_note
John,Smith,john@acme.com,Acme Corp,CEO,SaaS,Saw your product hunt launch
```

Target: 500 leads minimum before first send.

### Day 14-21: First campaign launch (5-8 hours)

**Task 7: Write sequences using 6-questions framework**

The 6 questions every cold email answers (under 100 words total):
1. What you do
2. Who for
3. How
4. Problem solved
5. Proof (specific numbers)
6. ROI

Pre-built sequences in `EMAIL_SEQUENCES.md`:
- Sequence 1: App promotion (partner/affiliate) - 12-20% reply rate
- Sequence 2: Service sales (agency/freelance)
- Sequence 3: Lead gen offer (local businesses)
- Sequence 4: Newsletter cross-promotion

**Task 8: Load campaign into Instantly**

1. Upload lead list CSV
2. Select sequence (start with Sequence 1 or 2)
3. Set schedule: M-F, 8am-5pm recipient timezone
4. Set daily limit: 10-20/inbox initially (ramp up)
5. Enable A/B testing on subject lines (minimum)
6. Set follow-up delays: Email 2 at Day 2-3, Email 3 at Day 5-7

**Task 9: Launch and monitor**

First week metrics to track:
```
Open rate:     Target 50%+ (if below 30%, deliverability issue)
Reply rate:    Target 3-5% (if below 1%, copy issue)
Bounce rate:   Must be under 3% (if above, list quality issue)
Spam complaints: Must be under 0.1% (if above, STOP and fix)
```

### Week 3-4: Optimize and scale

**Task 10: Analyze and iterate**

After 500+ emails sent, analyze:
- Which subject line won A/B test?
- Which leads replied most (title, industry)?
- What objections came back?
- Which sequence step got most replies?

Optimize:
- Kill losing subject lines
- Double down on winning lead segments
- Rewrite email steps with low engagement
- Add LinkedIn touchpoints between emails

**Task 11: Add LinkedIn layer**

LinkedIn touchpoints between emails increase reply rates 2-3x:
```
Day 0:  Email 1 (opener)
Day 1:  LinkedIn connection request (personalized)
Day 3:  Email 2 (follow-up)
Day 5:  LinkedIn message (if connected)
Day 7:  Email 3 (breakup)
Day 10: LinkedIn voice note (if connected)
```

Templates: `LINKEDIN_TEMPLATES.md` (15 templates for different scenarios)

**Task 12: Scale volume**

Scaling math:
```
Month 1:  2 domains, 6 inboxes, 150/day → 3,000 emails/mo
Month 2:  4 domains, 12 inboxes, 400/day → 8,000 emails/mo
Month 3:  6 domains, 18 inboxes, 750/day → 15,000 emails/mo
```

Add domains gradually. Never more than 2 new domains per week.

---

## Revenue mechanics

### How money flows

Build lead list -> Send cold emails -> Replies come in -> Book calls -> Close deals -> Invoice via Stripe

OR for affiliate/promotion model:
Send outreach to influencers/creators -> They promote your app -> Track installs via affiliate link -> Pay per install/rev share -> Net revenue

### Pricing models

| Model | Price Range | Best For |
|-------|-------------|----------|
| Per-lead | $5-50/qualified lead | Lead gen agencies |
| Retainer | $1,000-5,000/mo | Ongoing outbound services |
| Commission | 10-30% of closed deal | High-ticket services |
| Affiliate recruitment | $0.50-2 per install | App promotion |
| Service sales | $500-5,000/project | Direct client work |

### First dollar timeline
Day 0-14: Setup + warmup. Day 14-21: First sends. Day 21-28: First replies. Day 28-42: First closed deal/payment.

---

## Scaling path

### $0-1K/mo (Month 1-2)
2 domains, 6 inboxes. 100-200 emails/day. 3-5% reply rate. 1-3 deals/mo. Focus: dialing in copy and targeting.

### $1-10K/mo (Month 2-4)
4-6 domains, 12-18 inboxes. 400-750 emails/day. Add LinkedIn touchpoints. Hire VA for list building ($200-400/mo). Focus: volume + conversion optimization.

### $10K+/mo (Month 4-6)
8+ domains, 25+ inboxes. 1,000+ emails/day. Clay for AI personalization ($149/mo). Multiple sequences for different ICPs. Full-time VA. Focus: systemize and delegate.

---

## Risk management

- **Deliverability drop:** Monitor daily. If open rates drop below 30%, pause sends, increase warmup, check DNS. Reference: `COLD_EMAIL_INFRASTRUCTURE_GUIDE.md`
- **Domain burned:** Rotate to new domain. Buy domains 30 days before you need them so they age properly.
- **Gmail complaint threshold (0.1%):** Keep complaint rate under 0.1%. Above this, Gmail blocks you. Use unsubscribe links.
- **LinkedIn restrictions:** Max 100 connection requests/week, 150 messages/week. Use Sales Navigator for higher limits.
- **CAN-SPAM compliance:** Include physical address, unsubscribe option. B2B cold email is legal in US with proper identification.
- **GDPR (EU leads):** Need legitimate interest basis. Include opt-out. Document basis for contact.

---

## Success metrics

| Metric | Good | Great | Kill |
|--------|------|-------|------|
| Open rate | 40% | 60%+ | <25% |
| Reply rate | 3% | 8%+ | <1% |
| Positive reply rate | 1.5% | 4%+ | <0.5% |
| Bounce rate | <3% | <1% | >5% |
| Meeting book rate | 20% of positive replies | 40%+ | <10% |
| Deal close rate | 15% of meetings | 30%+ | <10% |

Kill: 60 days with <$200 revenue and reply rates below 1%.
Scale: Reply rate >5% and revenue >$1K/mo -> add domains and volume.

---

## Cross-pollination

| Method | Synergy | How it stacks |
|--------|---------|---------------|
| MM001 APP_FACTORY | 90 | Recruit affiliates for app promotion |
| AI001 NICHE_EXPERTS | 90 | Expert persona adds authority to outreach |
| MM051 AI_AUTOMATION_AGENCY | 85 | Sell automation services via cold email |
| MM002 INFO_PRODUCTS | 85 | Sell courses/guides to cold leads |
| MM015 NEWSLETTER | 85 | Convert cold leads to newsletter subscribers |
| MM092 WEB_TO_APP_FUNNEL | 80 | Drive traffic to web funnels |
| CF006 CLIP_CHANNELS | 75 | Recruit clippers via outreach |
