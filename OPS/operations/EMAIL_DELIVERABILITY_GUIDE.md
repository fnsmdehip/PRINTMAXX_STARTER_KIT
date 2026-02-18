# Email Deliverability Guide

Complete guide to email infrastructure setup, warmup protocols, and list hygiene. Get to inbox, not spam.

---

## Email Infrastructure Setup

### Domain Configuration

**Required DNS Records**

| Record | Type | Purpose |
|--------|------|---------|
| SPF | TXT | Authorize sending servers |
| DKIM | TXT | Cryptographic signature |
| DMARC | TXT | Policy for failed auth |
| MX | MX | Receiving mail (if needed) |

### SPF Record Setup

```
v=spf1 include:_spf.google.com include:sendgrid.net ~all
```

**Components:**
- `v=spf1` - Version
- `include:domain.com` - Authorize sender's servers
- `~all` - Soft fail (recommended for warmup)
- `-all` - Hard fail (after warmup complete)

**Common Includes:**
- Google Workspace: `include:_spf.google.com`
- SendGrid: `include:sendgrid.net`
- Mailgun: `include:mailgun.org`
- Postmark: `include:spf.mtasv.net`
- Amazon SES: `include:amazonses.com`

### DKIM Setup

**Record format:**
```
selector._domainkey.yourdomain.com TXT "v=DKIM1; k=rsa; p=MIIBIjANBg..."
```

**Setup steps:**
1. Generate DKIM key pair in your ESP
2. Add public key as DNS TXT record
3. Verify in ESP dashboard
4. Test with mail-tester.com

### DMARC Setup

**Progressive DMARC Implementation:**

**Phase 1 (Monitoring):**
```
v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```

**Phase 2 (Quarantine):**
```
v=DMARC1; p=quarantine; pct=25; rua=mailto:dmarc@yourdomain.com
```

**Phase 3 (Reject):**
```
v=DMARC1; p=reject; rua=mailto:dmarc@yourdomain.com
```

**Timeline:**
- Week 1-2: Monitor (p=none)
- Week 3-4: Quarantine 25% (p=quarantine; pct=25)
- Week 5-6: Quarantine 100% (p=quarantine)
- Week 7+: Reject (p=reject)

---

## Domain Warmup Protocol

### New Domain Warmup Schedule

**Week 1: Foundation**

| Day | Emails/Day | Target |
|-----|------------|--------|
| 1 | 10-20 | Known contacts only |
| 2 | 20-30 | Known contacts only |
| 3 | 30-40 | Known contacts only |
| 4 | 40-50 | Known contacts + warm leads |
| 5 | 50-75 | Warm leads |
| 6-7 | Rest | No sending |

**Week 2: Building**

| Day | Emails/Day | Target |
|-----|------------|--------|
| 8 | 75-100 | Warm leads |
| 9 | 100-125 | Warm + engaged list |
| 10 | 125-150 | Engaged list |
| 11 | 150-200 | Engaged list |
| 12 | 200-250 | General list |
| 13-14 | Rest | No sending |

**Week 3-4: Scaling**

| Day | Emails/Day | Target |
|-----|------------|--------|
| 15-21 | 250-500 | General list |
| 22-28 | 500-1000 | Full list |

**Week 5+: Full Volume**
- Gradual increase to target volume
- Never increase more than 50% day-over-day
- Monitor metrics closely

### Warmup Best Practices

1. **Start with engaged users**
   - Previous openers/clickers
   - Recent signups
   - Known contacts

2. **Encourage replies**
   - Ask questions
   - Request feedback
   - Personal tone

3. **Monitor metrics**
   - Open rate > 30% = good
   - Bounce rate < 2% = good
   - Spam complaints < 0.1% = good

4. **Adjust based on signals**
   - Low opens = slow down
   - High bounces = pause and clean list
   - Spam complaints = stop immediately

### Automated Warmup Tools

| Tool | Price | Method |
|------|-------|--------|
| Warmbox | $15/mo | Auto-engagement network |
| Lemwarm | $29/mo | Peer-to-peer warmup |
| Mailreach | $25/mo | Warmup + monitoring |
| Instantly | $37/mo | All-in-one cold email |

**How they work:**
1. Connect your email account
2. Tool sends emails to network
3. Network opens, replies, marks important
4. Builds sender reputation automatically

---

## List Hygiene

### List Cleaning Schedule

| Frequency | Action |
|-----------|--------|
| Per send | Remove hard bounces immediately |
| Weekly | Review soft bounces (3+ = remove) |
| Monthly | Remove 90-day inactive |
| Quarterly | Full list verification |

### Email Verification Services

| Service | Price | Accuracy |
|---------|-------|----------|
| ZeroBounce | $15/10K | 99%+ |
| NeverBounce | $10/10K | 99%+ |
| Kickbox | $10/10K | 99%+ |
| Hunter | $49/mo | 95%+ |

**Verification categories:**
- Valid: Safe to send
- Invalid: Remove immediately
- Risky: Test with small batch
- Unknown: Verify manually or remove

### Re-engagement Campaign

**Before removing inactive subscribers:**

**Email 1 (Day 1):**
Subject: "Still interested in [topic]?"
Content: Simple yes/no ask

**Email 2 (Day 4):**
Subject: "Last chance to stay subscribed"
Content: What they'll miss + unsubscribe link

**Email 3 (Day 7):**
Subject: "Goodbye (unless...)"
Content: Final offer + auto-removal warning

**After 3 emails with no engagement:** Remove from list

---

## Cold Email Deliverability

### Domain Setup for Cold Email

**Recommended structure:**
- Main domain: company.com (never for cold email)
- Cold email domain: trycompany.com or getcompany.com
- Separate inbox per SDR

**Domain age matters:**
- New domains need 2-4 weeks warmup
- Aged domains (6+ months) start stronger
- Buy aged domains from marketplaces if needed

### Cold Email Volume Limits

| Account Age | Daily Limit | Weekly Limit |
|-------------|-------------|--------------|
| Week 1 | 10-20 | 50-100 |
| Week 2 | 20-40 | 100-200 |
| Week 3 | 40-75 | 200-400 |
| Week 4+ | 75-100 | 400-500 |
| Mature (3mo+) | 100-150 | 500-750 |

**Never exceed 150/day per inbox** - triggers spam filters

### Cold Email Technical Checklist

- [ ] Separate domain from main brand
- [ ] SPF, DKIM, DMARC configured
- [ ] 2-4 week warmup completed
- [ ] Custom tracking domain (not ESP default)
- [ ] Verified with mail-tester.com (score 9+)
- [ ] Bounce rate monitored per campaign
- [ ] Unsubscribe link included
- [ ] Physical address in footer

---

## Email Platform Setup

### Google Workspace

**Sending limits:**
- Free Gmail: 500/day
- Google Workspace: 2,000/day
- Via SMTP relay: 10,000/day

**Setup for cold email:**
1. Create workspace account
2. Use separate subdomain
3. Enable 2FA
4. Connect to warmup tool
5. Wait 2 weeks before sending

### Microsoft 365

**Sending limits:**
- Business Basic: 10,000/day
- Via SMTP: 30 messages/minute

**Deliverability notes:**
- Often better inbox placement than Gmail
- Less aggressive spam filtering
- Good for B2B outreach

### Transactional Email (ESP)

| Provider | Free Tier | Paid Starts |
|----------|-----------|-------------|
| SendGrid | 100/day | $19.95/mo |
| Postmark | 100/mo | $15/mo |
| Mailgun | 5K/mo | $35/mo |
| Amazon SES | 62K/mo | $0.10/1K |
| Resend | 3K/mo | $20/mo |

**Best practices:**
- Separate transactional from marketing
- Use dedicated IP at volume (50K+/mo)
- Monitor reputation dashboard

---

## Inbox Placement Testing

### Pre-Send Testing

**Test with every campaign:**
1. Send to seed list (10-20 test addresses)
2. Check inbox vs spam placement
3. Verify links work
4. Check rendering across clients

**Seed list should include:**
- Gmail (personal + workspace)
- Outlook (personal + 365)
- Yahoo
- Apple Mail
- ProtonMail

### Testing Tools

| Tool | Price | Features |
|------|-------|----------|
| Mail-tester.com | Free (3/day) | Score + recommendations |
| GlockApps | $79/mo | Inbox placement + monitoring |
| Litmus | $99/mo | Rendering + spam testing |
| Email on Acid | $99/mo | Rendering + accessibility |

### Reputation Monitoring

**Check regularly:**
- Google Postmaster Tools (free)
- Microsoft SNDS (free)
- Sender Score (free)
- Talos Intelligence (free)

**Healthy metrics:**
- Sender Score: 80+
- Google reputation: High
- Spam rate: <0.1%
- Bounce rate: <2%

---

## Troubleshooting Deliverability

### Common Issues

**Going to spam:**
1. Check authentication (SPF/DKIM/DMARC)
2. Review content for spam triggers
3. Check sender reputation
4. Reduce sending volume
5. Clean list of inactive users

**High bounce rate:**
1. Verify email list
2. Remove invalid addresses
3. Check for typos in collection
4. Use double opt-in

**Low open rates:**
1. Check inbox placement
2. Test subject lines
3. Verify "from" name recognition
4. Send at optimal times
5. Segment by engagement

### Spam Trigger Words

**Avoid in subject lines:**
- FREE, URGENT, ACT NOW
- $$$ or excessive punctuation!!!
- ALL CAPS
- "Re:" or "Fwd:" (when not genuine)
- Unsubscribe (ironically)

**Avoid in body:**
- Excessive links
- Large images with little text
- Hidden text
- Misleading subject lines
- Missing unsubscribe

### Blacklist Removal

**Check blacklist status:**
- MXToolbox.com
- MultiRBL.valli.org

**Removal process:**
1. Identify which blacklist
2. Find removal form on blacklist site
3. Explain what happened
4. Describe remediation steps
5. Request removal
6. Wait 24-72 hours

**Prevention:**
- Never buy email lists
- Always use double opt-in
- Remove inactive users regularly
- Monitor bounce rates closely

---

## Email Warmup Automation

### Daily Warmup Routine (Manual)

**Morning:**
1. Send 5-10 personal emails
2. Reply to any responses
3. Move any to Primary/Important

**Afternoon:**
1. Send 5-10 more personal emails
2. Check for replies
3. Mark important emails

**Track in spreadsheet:**
- Emails sent
- Replies received
- Open rate (if tracked)

### Warmup Tool Configuration

**Lemwarm/Warmbox settings:**
- Ramp-up speed: Slow
- Daily max: 30-40 during warmup
- Reply rate: 30-40%
- Positive interactions: Enable all

**After warmup (4 weeks):**
- Reduce warmup volume
- Maintain 10-20/day for reputation
- Monitor deliverability metrics

---

## Quick Reference

### DNS Records Checklist

```
SPF:  v=spf1 include:[your-esp] ~all
DKIM: [selector]._domainkey.[domain] TXT [public-key]
DMARC: v=DMARC1; p=none; rua=mailto:dmarc@[domain]
```

### Healthy Metrics

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Open rate | >25% | 15-25% | <15% |
| Bounce rate | <2% | 2-5% | >5% |
| Spam complaints | <0.1% | 0.1-0.3% | >0.3% |
| Unsubscribe rate | <0.5% | 0.5-1% | >1% |

### Emergency Response

**If deliverability drops:**
1. Stop all sending immediately
2. Check for blacklisting
3. Verify DNS records
4. Review recent content/lists
5. Reduce volume 50%
6. Focus on engaged users only
7. Gradually rebuild

---

Last updated: 2026-01-23
