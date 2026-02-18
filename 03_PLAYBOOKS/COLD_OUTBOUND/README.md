# Cold outbound system

Complete cold email, LinkedIn, and calling infrastructure for B2B lead generation.

## Quick start

1. Start with **infrastructure/** to set up domains and email
2. Use **lead_gen/** to build your prospect lists
3. Pick templates from **sequences/** for your offer type
4. Add **linkedin/** for multi-channel outreach
5. Track everything with **metrics/**
6. Supplement with **scripts/** for calling

## Folder structure

```
COLD_OUTBOUND/
├── infrastructure/         # Email setup and deliverability
│   ├── DOMAIN_SETUP.md      # Buying and configuring domains
│   ├── DNS_RECORDS.md       # SPF, DKIM, DMARC setup
│   ├── INBOX_WARMUP.md      # 30-day warmup protocol
│   ├── TOOL_COMPARISON.md   # Instantly vs Smartlead vs EmailBison
│   └── DELIVERABILITY_CHECKLIST.md
│
├── lead_gen/               # Building prospect lists
│   ├── APOLLO_GUIDE.md      # Using Apollo effectively
│   ├── LINKEDIN_SCRAPING.md # Sales Navigator tactics
│   ├── BUILTWITH_GUIDE.md   # Tech stack targeting
│   ├── TRIGGER_EVENTS.md    # Funding, hiring, review triggers
│   └── LIST_BUILDING_TEMPLATES.md
│
├── sequences/              # 20 email sequence templates
│   ├── agency_services_5touch.md
│   ├── saas_demo_5touch.md
│   ├── consulting_offer_5touch.md
│   ├── partnership_outreach_3touch.md
│   ├── podcast_guest_pitch_3touch.md
│   ├── ecommerce_services_5touch.md
│   ├── b2b_lead_gen_5touch.md
│   ├── recruiting_services_5touch.md
│   ├── web_dev_agency_5touch.md
│   ├── seo_services_5touch.md
│   ├── fractional_cxo_5touch.md
│   ├── hr_services_5touch.md
│   ├── pr_media_5touch.md
│   ├── coaching_programs_5touch.md
│   ├── it_managed_services_5touch.md
│   ├── accounting_services_5touch.md
│   ├── video_production_5touch.md
│   ├── real_estate_services_5touch.md
│   ├── legal_services_5touch.md
│   ├── investor_outreach_3touch.md
│   ├── freelance_services_4touch.md
│   ├── event_sponsorship_3touch.md
│   └── local_business_4touch.md
│
├── linkedin/               # LinkedIn outreach
│   ├── CONNECTION_STRATEGY.md
│   ├── MESSAGE_TEMPLATES.md
│   ├── CONTENT_FOR_AUTHORITY.md
│   └── AUTOMATION_SAFE.md
│
├── metrics/                # Tracking and optimization
│   ├── BENCHMARKS.md
│   ├── TRACKING_SETUP.md
│   ├── A_B_TESTING.md
│   └── OPTIMIZATION_PLAYBOOK.md
│
└── scripts/                # Call scripts
    ├── COLD_CALL_SCRIPT.md
    ├── VOICEMAIL_SCRIPT.md
    └── FOLLOW_UP_CALL_SCRIPT.md
```

## Key benchmarks

| Metric | Target | Good | Excellent |
|--------|--------|------|-----------|
| Open rate | 50%+ | 55% | 65%+ |
| Reply rate | 5%+ | 8% | 12%+ |
| Meeting rate | 1.5%+ | 2.5% | 4%+ |
| Bounce rate | < 2% | < 1% | < 0.5% |

## Infrastructure costs (500 emails/day)

| Item | Monthly cost |
|------|--------------|
| 10 domains | ~$8/month (annualized) |
| 25 Google Workspace inboxes | ~$180/month |
| Email tool (Instantly) | $97/month |
| Apollo Pro | $79/month |
| Email verification | ~$20/month |
| **Total** | ~$385/month |

## Getting started checklist

### Week 1: Infrastructure
- [ ] Buy 3-5 secondary domains
- [ ] Set up Google Workspace
- [ ] Configure DNS (SPF, DKIM, DMARC)
- [ ] Start inbox warmup

### Week 2-3: Warmup period
- [ ] Let warmup run (no cold sends yet)
- [ ] Set up Apollo account
- [ ] Build first ICP definition
- [ ] Write email sequences

### Week 4: Launch
- [ ] Export first list (500 verified leads)
- [ ] Start slow (50 emails/day)
- [ ] Ramp up over 2 weeks
- [ ] Add LinkedIn in parallel

### Ongoing
- [ ] Keep warmup running
- [ ] Track metrics weekly
- [ ] A/B test continuously
- [ ] Refresh lists monthly

## Tools used

**Email:**
- Instantly.ai (sending and warmup)
- Google Workspace (inboxes)
- ZeroBounce (verification)

**Lead data:**
- Apollo.io (contacts)
- LinkedIn Sales Navigator (targeting)
- BuiltWith (tech stack)

**LinkedIn:**
- Sales Navigator (research)
- Manual outreach (safest)
- Dux-Soup (automation, careful)

**Analytics:**
- Email tool dashboards
- Google Sheets (tracking)
- Optional: HubSpot CRM

## Compliance

**CAN-SPAM (US):**
- Clear sender identity
- Physical address in signature
- Honor opt-out requests
- Accurate subject lines

**GDPR (EU):**
- Legitimate interest basis for B2B
- Honor data requests
- Keep processing records

**Best practices:**
- Only contact business emails
- Remove bounces immediately
- Respect unsubscribe requests
- Don't scrape personal emails

---

Created: 2026-01-20
Last updated: 2026-01-20
