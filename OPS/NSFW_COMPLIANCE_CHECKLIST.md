# NSFW AI Persona Compliance Checklist

**For:** @GoddessAriaAI (and all future AI personas)
**Created:** 2026-02-27
**Review frequency:** Weekly (Sunday)
**Companion docs:** `MONEY_METHODS/AI_INFLUENCER/NSFW_SAFETY_EXECUTION_PLAN.md`, `AI_NSFW_EXECUTION_FULL.md`

---

## 1. FTC AI Content Disclosure

The FTC Act Section 5 prohibits deceptive practices. AI personas must disclose clearly.

- [ ] Bio states "AI-generated persona" or "AI persona"
- [ ] Bio states "Not a real person"
- [ ] Bio states "Operated by a human"
- [ ] Pinned post contains full FTC disclosure template
- [ ] Fanvue profile includes AI disclosure
- [ ] Every profile across all platforms has disclosure
- [ ] Affiliate links (if any) include "#ad" or "affiliate link" disclosure
- [ ] No income claims without substantiation
- [ ] Findom framing uses "gifts/tributes/support" not "investments/returns"

**FTC Disclosure Template:**
```
DISCLOSURE: This is an AI-generated persona. All content is created using artificial
intelligence tools. I am not a real person. A real human operates this account.
18+ ONLY. By engaging, you confirm you are 18 or older.
```

---

## 2. Twitter/X TOS Compliance

- [ ] Account marked as sensitive in Settings → Privacy → Content
- [ ] "Mark media as sensitive" enabled for all posts
- [ ] Bio clearly identifies as AI (Twitter allows AI accounts with disclosure)
- [ ] No explicit content in public timeline (use sensitive media tag)
- [ ] No spam behavior (auto-DM blasts, mass following, engagement pods)
- [ ] No impersonation of real people
- [ ] No purchased followers or engagement
- [ ] Rate limits respected (follows, posts, DMs)
- [ ] No use of Twitter API for prohibited purposes
- [ ] Content complies with Twitter's Sensitive Media Policy

**What triggers X enforcement (avoid these):**
- Unsolicited explicit content in replies to non-adult accounts
- Mass automated DMs with explicit content
- Impersonating a real person
- CSAM or anything resembling it
- Spam behavior patterns (bulk follow/unfollow, duplicate content)

---

## 3. Fanvue AI Persona Policies

Fanvue explicitly allows AI creators as of Feb 2026.

- [ ] Selected "AI Creator" category during signup
- [ ] AI creator badge enabled on profile
- [ ] KYC completed with operator's real identity
- [ ] AI disclosure in profile description
- [ ] All content tagged as AI-generated in metadata
- [ ] Payment method verified (Stripe/bank)
- [ ] Content within Fanvue's acceptable use policy
- [ ] No real person's likeness used in any content
- [ ] Subscriber age verification gate active

---

## 4. Age Verification Requirements

- [ ] **Platform-level:** Bio states "18+ ONLY"
- [ ] **Content-level:** All sensitive content behind platform age gates
- [ ] **DM-level:** Age check template used when age is unclear
- [ ] **Fanvue:** Age verification gate enabled for all paid tiers
- [ ] **Twitter:** Account set to sensitive content (requires age to view)
- [ ] No content that could appeal to or target minors
- [ ] No use of youthful/childlike aesthetics in AI generations
- [ ] All AI-generated characters appear clearly adult (25+ appearance)

---

## 5. Content Moderation Obligations

### Tier 1: Immediate Action (automated via nsfw_safety_system.py)
- [ ] Keyword blocklist active and up-to-date
- [ ] Auto-block triggers on CSAM-related terms
- [ ] All Tier 1 blocks logged to `escalation_log.jsonl`
- [ ] NCMEC reporting process documented and accessible

### Tier 2: Human Review
- [ ] Escalated messages reviewed within 24 hours
- [ ] Pattern offenders blocked after 3 violations
- [ ] Screenshots preserved for all escalations

### Tier 3: Monitoring
- [ ] Weekly review of interaction patterns
- [ ] Unusual behavior flagged for follow-up

### NCMEC Reporting (Federal Obligation)
Under 18 U.S.C. 2258A, any provider of an electronic communication service who obtains actual knowledge of CSAM must report to NCMEC.

- [ ] NCMEC CyberTipline bookmarked: https://report.cybertip.org
- [ ] Reporting process understood by all operators
- [ ] Any CSAM detection → report within 24 hours
- [ ] Preserve all evidence (do not delete the content before reporting)
- [ ] Document the report (date, reference number, content description)

---

## 6. Record-Keeping Requirements

### What to Retain
| Record Type | Location | Retention Period |
|-------------|----------|-----------------|
| All posted content | COMPLIANCE_RECORDS/ | 3 years minimum |
| Content generation prompts + seeds | COMPLIANCE_RECORDS/ | 3 years minimum |
| DM interaction logs | interaction_log.jsonl | 3 years minimum |
| Blocked user records | blocked_users.csv | 5 years |
| Escalation logs | escalation_log.jsonl | 5 years |
| Revenue records | LEDGER/REVENUE_TRACKER.csv | 7 years (tax) |
| Content approval decisions | content_approval_queue.csv | 3 years |
| FTC disclosure screenshots | COMPLIANCE_RECORDS/ | 3 years |

### How Records Are Maintained
- `nsfw_safety_system.py` auto-logs all interactions to JSONL
- Content approval queue tracked in CSV (human reviews)
- Git auto-backup runs daily at 9 PM (committed to repository)
- Manual backup: `python3 AUTOMATIONS/backup_system.py --full`

---

## 7. Privacy Policy Requirements

### Operator Privacy
- [ ] Operator's real identity NOT disclosed publicly (only to platforms via KYC)
- [ ] Business email used for inquiries (not personal email)
- [ ] No personal address, phone, or real name in any public profile
- [ ] Separate browser profile used for all NSFW account management

### Fan/Subscriber Data Handling
- [ ] Do not collect personal data beyond what platforms provide
- [ ] Do not share subscriber lists or data with third parties
- [ ] Do not screenshot or share private DM content externally
- [ ] If a subscriber requests data deletion, comply within 30 days
- [ ] No data sold or shared for marketing purposes

---

## 8. Audit Schedule

### Weekly Audit (Every Sunday)
```bash
python3 AUTOMATIONS/nsfw_safety_system.py --audit
python3 AUTOMATIONS/nsfw_safety_system.py --status
```

Check:
- [ ] Review `OPS/NSFW_SAFETY_AUDIT.md` output
- [ ] All blocked users logged correctly
- [ ] No unapproved content was posted
- [ ] DM interactions used templates only
- [ ] Escalation log reviewed — any Tier 1 events?
- [ ] Revenue tracked in LEDGER
- [ ] Disclosure still visible in all profiles

### Monthly Audit (1st of every month)
- [ ] Review full escalation log for patterns
- [ ] Update keyword blocklist if new threats identified
- [ ] Verify all platforms still have AI disclosure
- [ ] Check Fanvue payout records match LEDGER
- [ ] Review content approval queue for any stuck items
- [ ] Verify backup system ran successfully all month
- [ ] Update this checklist if regulations changed

### Quarterly Audit
- [ ] Review FTC enforcement actions for AI content (search FTC.gov)
- [ ] Review TAKE IT DOWN Act implementation status
- [ ] Check state-level deepfake law changes
- [ ] Review platform TOS updates (Twitter, Fanvue)
- [ ] Update compliance docs if any changes needed
- [ ] Full test of safety system: `python3 AUTOMATIONS/nsfw_safety_system.py --test`

---

## Quick Reference: What's Legal, What's Not

| Action | Status | Notes |
|--------|--------|-------|
| AI-generated NSFW content (original characters) | LEGAL | Must disclose as AI |
| Selling AI content on Fanvue | LEGAL | Fanvue allows AI creators |
| Using real person's likeness without consent | ILLEGAL | TAKE IT DOWN Act (May 2026) |
| Not disclosing AI-generated content | ILLEGAL | FTC deceptive practices |
| Failing to report CSAM | FEDERAL CRIME | 18 U.S.C. 2258A |
| Findom-style "tributes" with disclosure | LEGAL | Use "gift/tribute" not "investment" |
| Auto-blocking dangerous DM content | LEGAL + REQUIRED | Best practice |
| Live AI chatbot conversations in DMs | RISKY | Not doing this (template-only) |
| Cross-posting between Twitter and Fanvue | LEGAL | Follow each platform's rules |
