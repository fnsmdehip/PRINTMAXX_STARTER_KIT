# Email Warmup Protocols

**Updated:** 2026-01-20
**Purpose:** Step-by-step inbox warming procedures for cold email infrastructure

---

## Warmup Fundamentals

### Why Warmup Matters

New email accounts/domains have:
- No sending history
- No reputation with providers
- Default "suspicious" status
- High likelihood of spam folder

Warmup builds:
- Positive sending history
- Trust signals with Gmail/Outlook
- Inbox placement patterns
- Sender reputation score

### The Two-Phase Approach

**Phase 1: Establishment (Weeks 1-4)**
- Build initial reputation
- Very low volume
- Focus on engagement
- No cold sends

**Phase 2: Scaling (Weeks 5-8)**
- Gradually increase volume
- Start cold outreach
- Maintain warmup alongside
- Monitor metrics closely

---

## Pre-Warmup Setup Checklist

### Domain Preparation

- [ ] Domain purchased and registered
- [ ] Wait 48-72 hours for DNS propagation
- [ ] SPF record configured
- [ ] DKIM key generated and DNS record added
- [ ] DMARC record in monitor mode
- [ ] Email hosting connected (Google/M365)
- [ ] Inboxes created with professional names

### Inbox Setup

**Naming convention:**
```
firstname@domain.com
firstname.lastname@domain.com
flastname@domain.com
```

**Avoid:**
- Numbers in email (john123@)
- Generic addresses (sales@, info@)
- Overly long addresses

**Profile setup:**
- Add profile photo
- Set display name (First Last)
- Configure signature (simple, no images)
- Set timezone

### Pre-Warmup Actions (Week 0)

**Day 1-3:**
- Send 2-3 emails to personal accounts
- Reply to those emails
- Mark as important/star
- Create a calendar event with the email

**Day 4-7:**
- Subscribe to 5-10 newsletters
- Reply to a few
- Move newsletters from promotions to primary (Gmail)
- Send/receive emails with colleagues

---

## Protocol A: Manual Warmup (Free)

### Best For
- Budget-conscious operators
- Small scale (1-3 inboxes)
- Maximum control
- Highest quality signals

### Week 1: Foundation

**Daily actions (5-10 emails/day):**

| Day | Send To | Action |
|-----|---------|--------|
| 1 | Personal Gmail | Send, get reply |
| 2 | Personal Outlook | Send, get reply |
| 3 | Colleague | Send, get reply |
| 4 | Friend | Send, schedule calendar invite |
| 5 | Family | Send, get reply, forward |
| 6 | Personal accounts | Reply chains (3+ back and forth) |
| 7 | Mix | Continue conversations |

**Key behaviors:**
- Vary message length (short and medium)
- Include questions (get replies)
- Reply within hours (engagement signal)
- Open and read all responses

### Week 2: Expansion

**Daily actions (10-15 emails/day):**

| Day | Activity | Volume |
|-----|----------|--------|
| 1-2 | Continue conversations | 5/day |
| 1-2 | New outreach to contacts | 5/day |
| 3-4 | Subscribe to industry newsletters | 3-5 total |
| 3-4 | Reply to newsletters | 1-2/day |
| 5-7 | Mix of all above | 10-15/day |

**Additional actions:**
- Send a few longer emails (300+ words)
- Include links (to legitimate sites)
- Move emails between folders
- Star/mark important messages

### Week 3: Growth

**Daily actions (15-25 emails/day):**

| Type | Volume | Notes |
|------|--------|-------|
| Conversations | 5-8 | Ongoing threads |
| New contacts | 5-8 | People you know |
| Newsletters | 2-3 | Interact with |
| Business contacts | 3-5 | Vendors, partners |

**New behaviors:**
- Send emails at different times
- Use mobile and desktop
- Occasional longer emails
- Include attachments (small, legitimate)

### Week 4: Pre-Launch

**Daily actions (20-30 emails/day):**

| Type | Volume | Notes |
|------|--------|-------|
| All previous | 15-20 | Maintain |
| Light cold outreach | 5-10 | Very warm leads only |

**Cold test criteria:**
- People who opted in somewhere
- Referred contacts
- Recent event connections
- Very warm LinkedIn connections

### Post Week 4: Maintenance

**Ongoing (while sending cold):**
- 20-30% of daily volume = warm emails
- Continue conversations
- Reply to newsletters
- Engage with responses

---

## Protocol B: Automated Warmup

### Best For
- Scaling operations
- Multiple inboxes
- Less manual effort
- Consistent signals

### Automated Warmup Tools

| Tool | Cost | Included With | Features |
|------|------|---------------|----------|
| Instantly | Included | Platform subscription | Network warmup |
| Smartlead | Included | Platform subscription | AI warmup |
| Warmbox | $15/mo | Standalone | Large network |
| Mailwarm | $79/mo | Standalone | Premium network |
| Lemwarm | $29/mo | Lemlist subscription | Integrated |

### How Automated Warmup Works

```
┌─────────────────┐
│   Your Inbox    │
└────────┬────────┘
         │ Sends to
         ▼
┌─────────────────┐
│  Warmup Network │  (1000s of real inboxes)
│     Inboxes     │
└────────┬────────┘
         │ Auto-replies
         ▼
┌─────────────────┐
│   Your Inbox    │  (receives, opens, replies)
└─────────────────┘
```

**Actions automated:**
1. Emails sent from your inbox to network
2. Network inboxes open emails
3. Network inboxes reply
4. Network marks as important
5. Network moves from spam to inbox (if needed)
6. Your inbox receives positive signals

### Automated Warmup Settings

**Week 1-2 (Conservative):**
```
Daily warmup emails: 5-10
Ramp increase: 2/day
Reply rate target: 40-50%
Open rate target: 80%+
```

**Week 3-4 (Growth):**
```
Daily warmup emails: 15-25
Ramp increase: 3/day
Reply rate target: 35-45%
Open rate target: 75%+
```

**Week 5+ (Maintenance):**
```
Daily warmup emails: 20-30
Ramp increase: 0 (stable)
Reply rate target: 30-40%
Open rate target: 70%+
```

### Automated + Manual Hybrid (Recommended)

**Best approach:**
- Automated for baseline signals
- Manual for higher quality signals
- Combination builds strongest reputation

**Daily split:**
| Type | Volume | Purpose |
|------|--------|---------|
| Automated | 15-20 | Baseline engagement |
| Manual personal | 5-10 | High-quality signals |
| Cold outreach | 20-50 | Revenue generation |

---

## Protocol C: Inbox-as-a-Service

### Best For
- Immediate scale needs
- Skip warmup period
- Budget available
- Redundancy/backup

### Services

| Service | Cost | Warmup Included | Notes |
|---------|------|-----------------|-------|
| Mailforge | $3/inbox/mo | Pre-warmed | Popular choice |
| DeliverOn | $49/mo | Yes | Managed service |
| Mailscale | $5/inbox/mo | Pre-warmed | Newer option |

### Using Pre-Warmed Inboxes

**Day 1-3:**
- Receive inboxes
- Connect to sending platform
- Test with internal sends
- Verify deliverability (mail-tester)

**Day 4-7:**
- Start at 20-30 emails/day
- Monitor metrics closely
- Keep automated warmup running
- Adjust based on performance

**Week 2+:**
- Scale to 40-50/day if metrics good
- Maintain warmup (20% of volume)
- Monitor weekly

### Risks of Pre-Warmed

- Previous reputation unknown
- Shared IP concerns
- Service could shut down
- Less control

**Mitigation:**
- Use alongside self-warmed inboxes
- Don't rely on single service
- Monitor closely first 2 weeks
- Have backup ready

---

## Warmup Metrics & Monitoring

### Key Metrics to Track

| Metric | Week 1-2 | Week 3-4 | Week 5+ |
|--------|----------|----------|---------|
| Open rate | 80%+ | 70%+ | 60%+ |
| Reply rate | 50%+ | 40%+ | 30%+ |
| Spam rate | <0.1% | <0.1% | <0.1% |
| Bounce rate | <1% | <2% | <3% |

### Monitoring Tools

**Free:**
- Google Postmaster Tools (essential for Gmail)
- mail-tester.com (per-email scoring)
- Platform dashboards (Instantly, etc.)

**Paid:**
- GlockApps ($59/mo) - inbox placement
- Mailreach ($25/mo) - real-time monitoring

### Warning Signs

**Immediate action needed:**
- Open rate drops below 40%
- Spam complaints above 0.3%
- Bounce rate above 5%
- Emails landing in spam folder

### Recovery Protocol

If metrics drop:

1. **Stop cold sends immediately**
2. **Increase warmup to 80% of volume**
3. **Run only warm emails for 1-2 weeks**
4. **Check technical setup** (SPF/DKIM/DMARC)
5. **Verify email list quality**
6. **Gradually resume** at 50% previous volume

---

## Warmup Schedule Templates

### Template A: Solo Operator (2 Inboxes)

**Week 1-2:**
| Day | Inbox 1 | Inbox 2 | Total |
|-----|---------|---------|-------|
| Mon | 5 manual | 5 manual | 10 |
| Tue | 7 manual | 7 manual | 14 |
| Wed | 8 manual | 8 manual | 16 |
| Thu | 10 manual | 10 manual | 20 |
| Fri | 10 manual | 10 manual | 20 |

**Week 3-4:**
| Day | Inbox 1 | Inbox 2 | Total |
|-----|---------|---------|-------|
| Daily | 10 auto + 5 manual | 10 auto + 5 manual | 30 |

**Week 5+:**
| Day | Inbox 1 | Inbox 2 | Total |
|-----|---------|---------|-------|
| Daily | 15 warm + 25 cold | 15 warm + 25 cold | 80 |

### Template B: Scale Operation (5+ Inboxes)

**Week 1-2:**
- All inboxes: 5-10 automated warmup only
- Monitor deliverability

**Week 3-4:**
- Increase to 20 automated per inbox
- Add 5 manual per inbox
- Total: 125/day across 5 inboxes

**Week 5+:**
- 20 warm + 30 cold per inbox
- Total: 250/day across 5 inboxes
- Rotate inboxes weekly

---

## Common Warmup Mistakes

### Mistake 1: Skipping Warmup

**Problem:** New domain/inbox goes straight to cold sends
**Result:** Immediate spam folder, possible suspension
**Fix:** Always warm minimum 2 weeks

### Mistake 2: Ramping Too Fast

**Problem:** Volume increases too quickly
**Result:** Triggers spam filters
**Fix:** Increase by 3-5 emails/day maximum

### Mistake 3: Stopping Warmup After Start

**Problem:** Warmup stops once cold sends begin
**Result:** Reputation decay
**Fix:** Maintain 20-30% warmup ongoing

### Mistake 4: Ignoring Metrics

**Problem:** Not monitoring deliverability
**Result:** Problems compound unnoticed
**Fix:** Weekly metric review minimum

### Mistake 5: Single Inbox Reliance

**Problem:** All volume through one inbox
**Result:** Single point of failure
**Fix:** Distribute across 3+ inboxes minimum

---

## Advanced: Multi-Domain Warmup Strategy

### Setup

```
Domain 1: yourbrand.io
  - inbox1@yourbrand.io
  - inbox2@yourbrand.io

Domain 2: getyourbrand.com
  - inbox1@getyourbrand.com
  - inbox2@getyourbrand.com

Domain 3: yourbrandhq.com
  - inbox1@yourbrandhq.com
  - inbox2@yourbrandhq.com
```

### Staggered Warmup

| Week | Domain 1 | Domain 2 | Domain 3 |
|------|----------|----------|----------|
| 1 | Start warmup | Purchase | - |
| 2 | Continue | DNS setup | Purchase |
| 3 | Light sends | Start warmup | DNS setup |
| 4 | Scale | Continue | Start warmup |
| 5 | Full scale | Light sends | Continue |
| 6 | Maintain | Scale | Light sends |

**Benefit:** Continuous pipeline of ready inboxes

### Rotation Strategy

Once all domains warmed:
- Rotate primary sending domain weekly
- Rest domains for 1-2 weeks between campaigns
- Monitor each domain separately
- Retire underperformers, add new ones

---

## Warmup Checklist

### Before Starting

- [ ] Domain aged 2+ weeks
- [ ] SPF/DKIM/DMARC configured
- [ ] Email hosting connected
- [ ] Inbox profiles complete
- [ ] Warmup tool connected (if using)
- [ ] Monitoring tools set up

### Weekly During Warmup

- [ ] Check open rates
- [ ] Check reply rates
- [ ] Verify no spam complaints
- [ ] Run mail-tester.com test
- [ ] Adjust volume as needed

### Before Starting Cold Sends

- [ ] 4+ weeks of warmup completed
- [ ] Open rate >60%
- [ ] Reply rate >30%
- [ ] No spam folder issues
- [ ] Passing mail-tester.com (8+/10)
- [ ] Google Postmaster shows green

---

**Related docs:**
- DELIVERABILITY_2026.md - Full deliverability guide
- SCRIPT_TEMPLATES.md - Email copy templates
- LEAD_SOURCES.md - Where to find leads
- SEQUENCES.md - Multi-touch frameworks
