# Cold Outbound Research Loop

## Mission
Research cold outbound tactics, deliverability updates, platform limits, and tool changes.

## What to Research Each Iteration

Pick ONE of these categories (rotate through them):

### 1. EMAIL_DELIVERABILITY
- Check for Gmail/Outlook policy changes in 2026
- DMARC/SPF/DKIM enforcement updates
- Inbox placement rates by provider
- Warmup protocol changes (what still works)
- New tools for deliverability monitoring

### 2. COLD_EMAIL_TACTICS
- Reply rate benchmarks (target 10%+)
- Subject line patterns that work now
- Personalization tactics (AI vs manual)
- Sequence length optimization (how many emails)
- Best send times by industry

### 3. LINKEDIN_OUTREACH
- Connection request limits (current safe limits)
- InMail alternatives
- Voice note effectiveness data
- Profile optimization for outbound
- Automation tool safety (what gets flagged)

### 4. COLD_CALLING
- VA cold calling scripts that convert
- Best times to call by industry
- Voicemail drop services
- Phone verification/validation
- Parallel dialer tools

### 5. TOOL_UPDATES
- Instantly.ai updates
- Smartlead updates
- Apollo.io changes
- Clay enrichment updates
- New outbound tools launched

## Output Format

For each finding, append to LEDGER/ALPHA_STAGING.csv:
```
alpha_id,source,source_url,category,title,description,actionable_steps,effort_level,roi_potential,risk_level,applies_to_niches,status,reviewed_date,reviewer_notes
```

Category: OUTBOUND
Status: PENDING_REVIEW

## State File
Read `.ralph/progress.md` first to see what categories have been covered.
Update it after each iteration with:
- Category researched
- Number of findings
- Key insight

## Rules
1. ONLY append to CSV files, never overwrite
2. Check for duplicates before adding (grep source_url)
3. Each finding needs specific numbers or proof
4. No vague "experts say" findings
5. Mark findings that need human verification
