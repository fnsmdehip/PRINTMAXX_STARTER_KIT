# Compliance Scanner

## Overview

Scans AI-generated content for FTC disclosure requirements, platform TOS violations, earnings claim substantiation, health claims, PII exposure, and fake social proof. Designed for content operations that produce at scale -- social posts, email sequences, landing pages, product listings -- where a single compliance miss can trigger legal liability or platform bans. Returns severity-scored violation reports with auto-fix suggestions.

## Architecture

The scanner is a rule-based engine with categorized violation detection and a fix suggestion pipeline.

```
Content Input (files, directories, or text)
        │
        ▼
┌────────────────────────┐
│    Rule Engine          │
│  ┌──────────────────┐  │
│  │ FTC Affiliate     │  │  -- detects affiliate links without disclosure
│  │ Income Claims     │  │  -- flags earnings claims without disclaimers
│  │ Health Claims     │  │  -- catches medical/health claims
│  │ Fake Social Proof │  │  -- spots fabricated testimonials/numbers
│  │ PII Exposure      │  │  -- finds emails, phones, SSN patterns
│  │ CAN-SPAM          │  │  -- checks email compliance requirements
│  │ Platform TOS      │  │  -- flags bot/automation language
│  └──────────────────┘  │
│           │             │
│     Match + Score       │
│           │             │
│     Fix Suggestions     │
└────────────────────────┘
        │
        ▼
Compliance Report (per-file violations, severity, suggested fixes)
```

**Rule categories and detection patterns:**

1. **FTC Affiliate Disclosure** -- regex patterns detect affiliate/referral/commission language. Cross-checks for proper disclosure patterns (#ad, affiliate disclosure statement, paid partnership). Violation if affiliate language present without disclosure.

2. **Income/Earnings Claims** -- detects dollar amounts with time periods ("$X/month"), income claims ("made $X"), figure references ("6-figure"), and lifestyle claims ("quit my 9-5"). Cross-checks for disclaimer patterns ("results may vary", "not typical", "individual results").

3. **Health Claims** -- catches cure/treat/prevent language, "clinically proven" claims, doctor recommendations, weight loss guarantees, immunity claims.

4. **Fake Social Proof** -- flags fabricated metrics ("X businesses already signed up", "trusted by X+ companies", "join X+ others") when no verification data exists.

5. **PII Exposure** -- regex detection of email addresses, phone numbers, and SSN-format patterns in content destined for public channels.

6. **CAN-SPAM Compliance** -- for email content, checks for required unsubscribe mechanism, physical address, and sender identity.

7. **Platform TOS Red Flags** -- detects mass/bulk automation language, bot references, fake engagement language that would trigger platform enforcement.

**Severity scoring:**

| Severity | Meaning | Example |
|----------|---------|---------|
| CRITICAL | Legal liability, immediate fix required | Income claim without disclaimer |
| HIGH | Platform ban risk | Bot/automation language in public post |
| MEDIUM | Compliance gap, should fix | Affiliate link without #ad |
| LOW | Best practice, recommended | Missing "results may vary" on case study |

## Required Inputs

- **Content files** -- any text-based content files: markdown, text, HTML. Supports scanning individual files, directories, or specific content types (social posts, emails, landing pages).
- **File type context** -- the scanner adjusts rules based on content type. Email content triggers CAN-SPAM checks. Social posts trigger platform TOS checks. Landing pages trigger all checks.

## Outputs

- **Compliance report** -- per-file breakdown of violations with:
  - Rule category (FTC, INCOME_CLAIM, HEALTH_CLAIM, FAKE_PROOF, PII, CANSPAM, PLATFORM_TOS)
  - Severity level (CRITICAL, HIGH, MEDIUM, LOW)
  - Matched text (the specific content that triggered the violation)
  - Line number and file path
  - Suggested fix (specific rewrite or addition to make the content compliant)
- **Summary statistics** -- total violations by category and severity across all scanned files
- **Auto-fix output** (when `--fix` flag is used) -- rewrites content with compliant alternatives where possible (adds disclosures, adds disclaimers, redacts PII)

## Setup

1. **Place the scanner in your automation directory:**
   ```
   project/
   ├── AUTOMATIONS/
   │   └── compliance_scanner.py
   └── CONTENT/
       ├── social/     (social media posts)
       ├── email/      (email sequences)
       └── landing/    (landing pages)
   ```

2. **No external dependencies required.** The scanner uses Python standard library only (re, csv, json, pathlib).

3. **Configure content directories** -- update the BASE path in the scanner to point to your project root. All path operations are guardrailed to the project directory.

4. **(Optional) Add to your CI/CD or cron:**
   ```bash
   # Daily compliance audit
   0 6 * * * python3 AUTOMATIONS/compliance_scanner.py --audit-all
   ```

5. **(Optional) Wire into your content pipeline** -- run the scanner automatically before any content is queued for posting or sending.

## Example Usage

Scan all social media content:
```bash
python3 compliance_scanner.py --scan-content CONTENT/social/
```

Scan email sequences for CAN-SPAM compliance:
```bash
python3 compliance_scanner.py --scan-emails AUTOMATIONS/outreach/
```

Scan a specific file:
```bash
python3 compliance_scanner.py --scan-file CONTENT/social/posting_queue/tweet_001.txt
```

Run a full audit across all content directories:
```bash
python3 compliance_scanner.py --audit-all
```

Auto-fix compliance issues where possible:
```bash
python3 compliance_scanner.py --fix CONTENT/social/posting_queue/tweet_001.txt
```

## Key Patterns

- **Rule registry architecture** -- each compliance category is defined as a set of detection patterns (regex) and corresponding disclosure/disclaimer patterns. Adding a new rule category means adding two lists: what to detect and what constitutes compliance.
- **Cross-check validation** -- the scanner does not simply flag keywords. It checks for the presence of affiliate language AND the absence of disclosure. Income claims are only flagged when they lack corresponding disclaimers. This reduces false positives.
- **Severity scoring** -- violations are scored by legal and operational risk. CRITICAL violations (income claims without disclaimers) are differentiated from LOW violations (missing best-practice language). This lets teams prioritize fixes.
- **Auto-fix suggestions** -- for each violation type, the scanner generates a specific suggested fix: "Add '#ad' to the beginning of this post", "Append 'Results may vary. This is not typical.' after the earnings claim", "Redact the email address on line 14."
- **Content-type-aware scanning** -- email content triggers CAN-SPAM checks that don't apply to social posts. Landing pages trigger fake social proof checks that don't apply to internal docs. The scanner adjusts its rule set based on content context.
- **Path guardrails** -- inherited from the project's safety system. The scanner only reads files within the project root. External paths are blocked.

## Limitations

- **Regex-based, not semantic.** The scanner catches pattern matches, not contextual meaning. A satirical post that says "I made $1M" as a joke will be flagged the same as a genuine earnings claim. Human review is still required for edge cases.
- **No image/video scanning.** The scanner only processes text content. Earnings screenshots, video testimonials, and image-based claims require separate tooling.
- **US-centric rules.** FTC and CAN-SPAM rules are US regulations. International compliance (GDPR, ASA, ACCC) requires additional rule sets not included by default.
- **Auto-fix is conservative.** The fix suggestions add disclosures and disclaimers but do not rewrite core claims. A misleading claim with a disclaimer is still potentially non-compliant -- the scanner flags this but cannot judge intent.
- **No platform API verification.** The scanner checks content text for TOS violations but does not verify against live platform rules. Platform TOS changes faster than regex patterns.
- **PII detection has false positives.** Phone number patterns can match non-phone numerical sequences. Email patterns are more reliable but can match code examples.
