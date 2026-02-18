# PRINTMAXX Emergency Procedures

**Purpose:** Handle crises quickly without panic
**Rule:** Document everything. Every emergency teaches something.

---

## Account Banned/Restricted

### X/Twitter Account Suspended

**Severity:** HIGH
**Impact:** Audience access, lead generation, brand presence

**Immediate actions (first hour):**
1. Do NOT create a new account (can get IP banned)
2. Screenshot the suspension notice
3. Document last activities before suspension
4. Check email for suspension reason

**Appeal process:**
1. Go to help.twitter.com/forms/account-access
2. Submit appeal with:
   - Account username
   - Email associated
   - Clear, polite explanation
   - Statement you'll comply with rules
3. Wait 24-48 hours for response
4. If denied, submit second appeal with more detail

**While waiting:**
- Communicate via email list (always have a backup channel)
- Post update on secondary platforms
- Do NOT mention suspension publicly (can hurt appeal)
- Review Twitter rules to identify potential violation

**Recovery plan:**
- If restored: Post normally, avoid whatever triggered suspension
- If permanent: Start fresh account, rebuild slowly, different approach
- Update SOPs to prevent recurrence

### Email Account Issues (Deliverability/Blacklist)

**Severity:** HIGH
**Impact:** Revenue, customer communication, lead nurturing

**Immediate actions:**
1. Check if you can still send (send test to yourself)
2. Check blacklist status: mxtoolbox.com/blacklists.aspx
3. Review bounce rates in email provider dashboard
4. Stop all campaigns until diagnosed

**Common causes:**
- High bounce rate (>5%)
- High spam complaints (>0.1%)
- Purchased or scraped list used
- Sudden volume increase
- Missing authentication (SPF/DKIM/DMARC)

**Recovery steps:**
1. Clean email list (remove bounces, inactive)
2. Request delisting from blacklists (each has a form)
3. Reduce sending volume temporarily
4. Warm up domain again slowly
5. Monitor closely for 2 weeks

**Prevention:**
- Regular list cleaning
- Double opt-in for all signups
- Warm up new domains properly
- Never buy email lists

### Payment Processor (Stripe) Issues

**Severity:** CRITICAL
**Impact:** Revenue stops immediately

**Immediate actions:**
1. Check Stripe dashboard for account status
2. Look for emails from Stripe explaining issue
3. Identify any flagged payments or chargebacks

**If account restricted:**
1. Respond to any Stripe requests immediately
2. Provide requested documentation promptly
3. Do not process payments through other means
4. Contact support if no clear reason given

**While restricted:**
- Pause any paid ads (no point driving traffic)
- Communicate with customers waiting on orders
- Prepare alternative payment method (PayPal backup)
- Do NOT try to open new Stripe account

**Prevention:**
- Keep chargeback rate under 1%
- Have clear refund policy
- Deliver what you promise
- Respond to disputes quickly

---

## Technical Emergencies

### Site Down

**Severity:** HIGH
**Impact:** Lost leads, lost sales, damaged credibility

**Diagnostic steps (5 min max):**
1. Check if it's you or the site: downforeveryoneorjustme.com
2. Check hosting status page (Vercel, Netlify, etc.)
3. Check domain status (did it expire?)
4. Check for deployment errors

**If hosting issue:**
1. Check hosting provider status page
2. Wait for their resolution (usually fast)
3. Tweet about it if extended (transparency)

**If deployment issue:**
1. Roll back to last working deployment
2. Check build logs for errors
3. Fix and redeploy

**If domain issue:**
1. Check domain registrar
2. Renew if expired
3. Check DNS settings

**Communication:**
- If down >30 min: Tweet brief update
- If down >2 hours: Email subscribers
- Always follow up when resolved

**Prevention:**
- Enable uptime monitoring (UptimeRobot, free)
- Auto-renew domain
- Test deployments before pushing
- Keep backup of last working deployment

### Database/Data Loss

**Severity:** CRITICAL
**Impact:** Customer data, content, business records

**Immediate actions:**
1. Stop any processes that might cause more damage
2. Assess what's lost (check backups)
3. Do NOT try to recover without a plan

**Recovery:**
1. Restore from most recent backup
2. Identify what happened between backup and now
3. Manually recover if possible
4. Document gaps

**If no backup exists:**
1. Check if hosting provider has snapshots
2. Check if any team member has local copy
3. Reconstruct from emails, documents, etc.
4. Accept loss and move forward

**Prevention:**
- Automated daily backups
- Test restoration quarterly
- Multiple backup locations
- Version control for all code

### Lead Capture Broken

**Severity:** HIGH
**Impact:** Lost leads, wasted traffic

**Diagnosis:**
1. Test the form yourself
2. Check form provider status
3. Check if webhook is working
4. Check LEDGER/leads.csv for recent entries

**Common causes:**
- Form provider API down
- Webhook URL changed
- CSV file locked or corrupted
- JavaScript error blocking form

**Fix:**
1. Identify broken component
2. Fix or use backup method
3. Test thoroughly
4. Monitor for 24 hours

**Estimate lost leads:**
- Traffic during outage x conversion rate = missed leads
- Document in incident report

---

## Reputation Emergencies

### Negative Publicity

**Severity:** MEDIUM to HIGH
**Impact:** Brand reputation, trust, future sales

**Assessment (before reacting):**
1. What specifically is being said?
2. Is it accurate criticism or false claims?
3. How much reach does it have?
4. Is it growing or dying down?

**Response framework:**

**If criticism is valid:**
1. Acknowledge publicly and quickly
2. Apologize sincerely (no "sorry if you were offended")
3. Explain what you're doing to fix it
4. Follow through on promises
5. Follow up publicly when fixed

**If criticism is false:**
1. Correct factual errors calmly with evidence
2. Do NOT get emotional or defensive
3. Take detailed response to DMs if possible
4. Document everything for potential escalation

**If it's a personal attack:**
1. Do not engage publicly
2. Block and report if appropriate
3. Let community defend you (if they will)
4. Move on

**Never do:**
- Delete legitimate criticism (makes it worse)
- Attack the critic personally
- Lie or make excuses
- Ignore significant criticism

### Competitor Attack

**Severity:** MEDIUM
**Impact:** Market position, customer confidence

**Response:**
1. Assess accuracy of claims
2. If false: One clear, factual correction, then move on
3. If true: Address the underlying issue
4. Never attack back publicly
5. Let your work speak for itself

**Best response:** Ship something better than yesterday.

### Customer Complaint Goes Viral

**Severity:** HIGH
**Impact:** Trust, sales, brand

**Immediate:**
1. Reach out to customer directly (DM, email)
2. Resolve their issue generously
3. If resolved, ask (don't demand) if they'd update publicly
4. Post your own brief, factual response publicly

**Response template:**
"We messed up here and [customer] was right to be frustrated. We've [specific resolution]. We're [what we're doing to prevent this]. Thanks for holding us accountable."

---

## Financial Emergencies

### Refund Requests

**Severity:** LOW to MEDIUM
**Impact:** Revenue, potential for chargebacks

**Standard process:**
1. Acknowledge request within 24 hours
2. Ask for reason (optional, helps improve)
3. Process refund within stated policy timeline
4. Send confirmation
5. Log in LEDGER for analysis

**Refund policy guidelines:**
- Clear timeline (7-30 days typical)
- Clear conditions (used vs unused)
- Easy process (don't make them fight for it)

**When to say no:**
- Outside refund window AND product delivered/consumed
- Clear abuse pattern (serial refunders)
- Fraud indicators

**When to say yes anyway:**
- High-value customer relationship at stake
- Public complaint risk
- You genuinely didn't deliver value
- Cost of fight > cost of refund

**If customer threatens chargeback:**
1. Refund immediately (chargeback fees are expensive)
2. Chargebacks hurt your processor standing
3. Not worth fighting unless clear fraud

### Cash Flow Crisis

**Severity:** CRITICAL
**Impact:** Business survival

**Immediate actions:**
1. Calculate exact runway (cash / monthly burn)
2. List all upcoming required expenses
3. Identify what can be cut or delayed

**Revenue options:**
- Offer discount for annual prepay
- Launch quick paid offering
- Sell consulting/services
- Affiliate promotions

**Cost cutting:**
- Pause all paid ads
- Downgrade tools to free tiers
- Pause any contractors
- Cancel unused subscriptions

**If runway < 30 days:**
- Honest assessment: pivot or shutdown?
- If pivot: What's the fastest path to revenue?
- If shutdown: How to exit gracefully?

---

## Emergency Response Checklist

For any emergency:

- [ ] Stop and breathe (2 minutes)
- [ ] Assess severity (1-5 scale)
- [ ] Identify immediate actions (next 1 hour)
- [ ] Communicate to affected parties
- [ ] Execute fixes
- [ ] Document what happened
- [ ] Create prevention plan
- [ ] Update SOPs

---

## Incident Report Template

Save to `OPS/logs/incidents/[DATE]-[type].md`:

```markdown
# Incident Report

**Date:**
**Type:**
**Severity:** 1-5 (5=critical)
**Duration:**
**Impact:**

## What Happened


## Timeline
- HH:MM -
- HH:MM -
- HH:MM -

## Root Cause


## Resolution


## Lessons Learned


## Prevention Measures


## Follow-up Actions
- [ ]
```

---

## Emergency Contacts

Document these somewhere secure:

- Hosting provider support:
- Domain registrar:
- Email provider support:
- Payment processor:
- Accountant/lawyer (if applicable):

---

## Prevention Mindset

Best emergency response is prevention:

1. **Backups** - Daily, tested quarterly
2. **Monitoring** - Uptime alerts, error tracking
3. **Redundancy** - Multiple channels for everything important
4. **Documentation** - SOPs for common issues
5. **Cash reserve** - 3-6 months runway minimum
6. **Reputation buffer** - Build goodwill before you need it
