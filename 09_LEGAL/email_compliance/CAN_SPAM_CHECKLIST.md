# CAN-SPAM Compliance Checklist

**US Email Marketing Requirements**

**IMPORTANT:** This is a reference guide, not legal advice. Consult with a qualified attorney for specific compliance questions.

---

## Overview

The CAN-SPAM Act (Controlling the Assault of Non-Solicited Pornography And Marketing Act) of 2003 sets rules for commercial email in the United States.

**Applies to:** Commercial messages promoting products, services, or commercial websites

**Penalties:** Up to $50,120 per violation (as of 2024)

---

## The 7 CAN-SPAM Requirements

### 1. No False or Misleading Header Information

**Required:**
- "From" name and email must accurately identify the sender
- "Reply-To" address must be valid
- Routing information must be accurate

**Compliant Examples:**
```
From: John Smith <john@[COMPANY NAME].com>
From: [COMPANY NAME] <newsletter@[COMPANY NAME].com>
From: [COMPANY NAME] Marketing <marketing@[COMPANY NAME].com>
```

**Non-Compliant Examples:**
```
From: "Your Friend" <random@gmail.com>  // Misleading
From: "Amazon" <scam@notamazon.com>     // Impersonation
From: "No Reply" <donotreply@fake.com>   // Not your real domain
```

### 2. No Deceptive Subject Lines

**Required:**
- Subject line must accurately reflect email content
- Cannot be misleading about contents or purpose

**Compliant Examples:**
```
Subject: 20% off your next purchase at [COMPANY NAME]
Subject: New blog post: How to increase productivity
Subject: Your weekly newsletter from [COMPANY NAME]
```

**Non-Compliant Examples:**
```
Subject: RE: Your request          // Implies existing conversation
Subject: URGENT: Account suspended // False urgency if not true
Subject: You won!                  // Misleading
Subject: Fwd: Important            // Fake forward
```

### 3. Identify the Message as an Advertisement

**Required:**
- Commercial nature must be clear
- Method is flexible (no specific language required)

**Acceptable Methods:**
- Clear promotional content
- "Advertisement" label
- Promotional layout/design
- Context makes commercial nature obvious

**Note:** Transactional or relationship emails may not need this disclosure (order confirmations, account updates, etc.)

### 4. Include Physical Postal Address

**Required:**
- Valid physical postal address in every commercial email
- Can be:
  - Street address
  - PO Box registered with USPS
  - Private mailbox registered with commercial mail receiving agency

**Placement:** Typically in email footer

**Example:**
```
[COMPANY NAME]
123 Main Street, Suite 100
Anytown, ST 12345
```

**Virtual Office/PO Box:**
```
[COMPANY NAME]
PO Box 1234
Anytown, ST 12345
```

### 5. Easy Opt-Out Mechanism

**Required:**
- Clear and conspicuous way to opt out
- Mechanism must work for at least 30 days after email is sent
- Cannot require:
  - Fee to unsubscribe
  - Personal information beyond email address
  - Visiting more than one page (beyond confirmation page)
  - Steps other than replying to email or visiting single web page

**Best Practices:**
```
[Unsubscribe from this list]
[Manage email preferences]
[Update your subscription settings]
```

**One-Click Unsubscribe:**
- Recommended for improved deliverability
- Required by Google/Yahoo as of February 2024

### 6. Honor Opt-Outs Promptly

**Required:**
- Process opt-out requests within 10 business days
- Cannot charge fee for processing
- Cannot require additional information
- Cannot sell or transfer email address after opt-out request

**Best Practice:**
- Process immediately (automated)
- Send confirmation of unsubscribe
- Maintain suppression list indefinitely

### 7. Monitor Third Parties

**Required:**
- You are responsible for compliance even if you hire others to send emails
- Cannot contract away legal responsibility

**Your Responsibility:**
- Ensure email service providers are compliant
- Monitor affiliate emails promoting your products
- Review any co-marketing arrangements

---

## Pre-Send Compliance Checklist

Use this checklist before every email campaign:

### Header Information
- [ ] "From" name accurately identifies sender
- [ ] "From" email uses legitimate domain
- [ ] "Reply-To" address is monitored and valid

### Subject Line
- [ ] Accurately reflects email content
- [ ] No false claims or misleading statements
- [ ] No fake RE: or FWD: prefixes

### Email Content
- [ ] Commercial nature is clear
- [ ] Physical postal address included
- [ ] Address is in visible location (not hidden)

### Unsubscribe Mechanism
- [ ] Clear unsubscribe link present
- [ ] Link is functional and tested
- [ ] No requirements beyond email address
- [ ] Opt-out mechanism will work for 30+ days
- [ ] System processes opt-outs within 10 days (ideally immediately)

### List Management
- [ ] Sending only to opted-in recipients
- [ ] Suppression list is up to date
- [ ] No purchased lists being used (risky)

### Third-Party Compliance
- [ ] ESP (email service provider) is reputable
- [ ] Any affiliates are compliant
- [ ] Co-marketing partners follow rules

---

## Transactional vs. Commercial Emails

### Transactional/Relationship Emails

**Definition:** Primary purpose is to facilitate or confirm a transaction, or update about an ongoing relationship

**Examples:**
- Order confirmations
- Shipping notifications
- Password resets
- Account statements
- Product updates (for purchased products)
- Security alerts

**CAN-SPAM Requirements:**
- Must not have false/misleading routing info
- Can include some commercial content, but primary purpose must be transactional

### Commercial Emails

**Definition:** Primary purpose is to advertise or promote commercial product or service

**Examples:**
- Newsletters with promotional content
- Sale announcements
- Product recommendations
- Abandoned cart emails (usually commercial)
- Re-engagement emails

**CAN-SPAM Requirements:**
- All 7 requirements apply

### Mixed Content Emails

If an email contains both transactional and commercial content:

**Primary Purpose Test:**
- Would a recipient reasonably conclude the primary purpose is commercial?
- What is in the subject line?
- What appears first in the body?

**When in doubt:** Treat as commercial and comply with all requirements.

---

## Common Violations to Avoid

### High-Risk Practices

| Practice | Risk Level | Issue |
|----------|-----------|-------|
| Purchased email lists | HIGH | Recipients did not consent |
| Misleading subject lines | HIGH | Direct CAN-SPAM violation |
| No unsubscribe link | HIGH | Direct CAN-SPAM violation |
| Slow opt-out processing | MEDIUM | 10-day limit |
| No physical address | MEDIUM | Direct CAN-SPAM violation |
| Affiliate spam | MEDIUM | You may be liable |

### Technically Compliant but Problematic

- Hiding unsubscribe in tiny text
- Multi-step unsubscribe process
- Requiring login to unsubscribe
- "Preferences" page with no clear unsubscribe
- Confirming unsubscribe via email only (should also work via web)

---

## Email Footer Template

```
---

[COMPANY NAME]
[123 Main Street, Suite 100 | Anytown, ST 12345]

You received this email because you [signed up for our newsletter / made a purchase / etc.].

[Unsubscribe] | [Manage Preferences] | [View in Browser]

© [YEAR] [COMPANY NAME]. All rights reserved.
```

**Detailed Footer:**
```
---

[COMPANY NAME] | [WEBSITE URL]
[123 Main Street, Suite 100, Anytown, ST 12345]

Why did I get this email?
You are receiving this because you subscribed to [LIST NAME] on [DATE/WEBSITE].

Don't want these emails? [Unsubscribe instantly]
Want fewer emails? [Manage your preferences]

Questions? Reply to this email or contact [SUPPORT EMAIL]

© [YEAR] [COMPANY NAME]. All rights reserved.
```

---

## Enforcement and Penalties

### Who Enforces CAN-SPAM?

- Federal Trade Commission (FTC)
- State Attorneys General
- Internet Service Providers (ISPs)

### Potential Penalties

- Up to $50,120 per email in violation
- Additional penalties for aggravated violations:
  - Harvesting email addresses
  - Generating addresses using dictionary attacks
  - Using scripts to register for email accounts
  - Relaying through others' computers without permission

### Deceptive Acts

Additional penalties under FTC Act Section 5 for deceptive practices.

---

## Documentation Best Practices

### Keep Records Of:

1. **Consent Records**
   - When each subscriber opted in
   - How they opted in (form, checkbox, etc.)
   - What they consented to receive

2. **Email Content**
   - Archive of all sent campaigns
   - Subject lines
   - Send dates

3. **Opt-Out Processing**
   - Unsubscribe requests and processing dates
   - Suppression list management

4. **Compliance Procedures**
   - Written policies
   - Staff training records
   - Third-party agreements

**Retention Period:** At least 3 years recommended

---

## Quick Reference Card

| Requirement | What to Do |
|-------------|------------|
| From Header | Use accurate sender name and email |
| Subject Line | Reflect actual content, no tricks |
| Ad Identification | Make commercial nature clear |
| Physical Address | Include in every email |
| Opt-Out | One-click, easy to find |
| Honor Opt-Outs | Process within 10 days |
| Third Parties | You are responsible for compliance |

---

## Additional Resources

- FTC CAN-SPAM Guide: https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business
- FTC Complaint: https://www.ftc.gov/complaint

---

*This checklist is provided for informational purposes only and does not constitute legal advice. Regulations may change. Consult with a qualified attorney to ensure compliance.*
