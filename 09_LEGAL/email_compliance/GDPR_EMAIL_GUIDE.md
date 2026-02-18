# GDPR Email Compliance Guide

**EU Email Marketing Requirements**

**IMPORTANT:** This is a reference guide, not legal advice. GDPR is complex and has significant penalties. Consult with a qualified attorney for specific compliance questions.

---

## Overview

The General Data Protection Regulation (GDPR) applies to processing personal data of individuals in the EU/EEA, regardless of where your business is located.

**Applies if you:**
- Have customers/subscribers in the EU/EEA
- Target EU/EEA residents with marketing
- Process data of EU/EEA individuals

**Key Difference from CAN-SPAM:**
- CAN-SPAM: Opt-out model (can email until they unsubscribe)
- GDPR: Opt-in model (need consent BEFORE emailing)

**Penalties:** Up to 20 million EUR or 4% of global annual turnover, whichever is higher

---

## Legal Bases for Email Marketing

Under GDPR, you need a legal basis to process personal data (including sending marketing emails).

### Option 1: Consent (Most Common for Marketing)

**Requirements for Valid Consent:**

| Requirement | Description |
|-------------|-------------|
| Freely given | No pressure, no bundling with other consents |
| Specific | Clear about what they're consenting to |
| Informed | Know who is contacting them and why |
| Unambiguous | Active opt-in (no pre-checked boxes) |
| Documented | You can prove consent was given |
| Withdrawable | Easy to revoke consent anytime |

**Valid Consent Examples:**

```
[ ] Yes, I would like to receive marketing emails from [COMPANY NAME]
    about [DESCRIPTION OF CONTENT].

I understand I can unsubscribe at any time.
```

```
[ ] Subscribe to our newsletter
    We'll send you [weekly/monthly] updates about [TOPICS].
    You can unsubscribe anytime.
```

**Invalid Consent Examples:**

```
[X] I agree to receive marketing emails  // Pre-checked - INVALID

"By creating an account, you consent to receive marketing emails"
// Bundled with service - INVALID

[ ] I agree to the Terms of Service and Privacy Policy and
    consent to receive marketing communications
// Combined consents - INVALID
```

### Option 2: Legitimate Interest

**More limited use for marketing. Requires:**

1. **Purpose Test:** Is there a legitimate interest?
2. **Necessity Test:** Is email marketing necessary for that interest?
3. **Balancing Test:** Does the individual's rights override your interest?

**When it might apply:**
- Existing customers, similar products
- B2B marketing in some cases
- Soft opt-in scenarios

**Documentation Required:**
- Legitimate Interest Assessment (LIA)
- Records demonstrating balancing test

**Safer approach:** Default to consent for email marketing.

---

## Consent Collection Best Practices

### Signup Forms

**Required Elements:**
- Unchecked checkbox (opt-in)
- Clear description of what they're subscribing to
- Link to privacy policy
- Company name
- How to unsubscribe

**Example Form:**

```
Subscribe to our newsletter

Email: [________________]

[ ] I want to receive weekly marketing emails from [COMPANY NAME]
    including product updates, tips, and occasional promotions.

By subscribing, you agree to our [Privacy Policy].
You can unsubscribe at any time.

[Subscribe]
```

### Double Opt-In (Highly Recommended)

**Process:**
1. User submits signup form
2. You send confirmation email
3. User clicks confirmation link
4. Subscription is activated

**Why use double opt-in:**
- Stronger proof of consent
- Cleaner email list
- Better deliverability
- Reduces complaints

**Confirmation Email Template:**

```
Subject: Please confirm your subscription

Hi [NAME],

Thanks for signing up! Please confirm your email address to complete
your subscription to [COMPANY NAME]'s newsletter.

[Confirm Subscription]

What to expect:
- [FREQUENCY] emails about [TOPICS]
- You can unsubscribe anytime

If you didn't sign up, just ignore this email.

[COMPANY NAME]
[ADDRESS]
```

### Consent Records

**Store the following for each subscriber:**
- Email address
- Date and time of consent
- Method of consent (which form, what URL)
- Exact wording shown at consent
- IP address (optional but helpful)
- Double opt-in confirmation date/time

**Record Example:**
```
{
  "email": "user@example.com",
  "consent_date": "2024-01-15T14:32:00Z",
  "consent_method": "website_form",
  "form_url": "https://[WEBSITE]/newsletter",
  "consent_text": "I want to receive weekly marketing emails...",
  "ip_address": "192.168.1.1",
  "double_optin_confirmed": "2024-01-15T14:45:00Z"
}
```

---

## Data Subject Rights for Email

### Right to Be Informed

**At collection, inform subscribers of:**
- Your identity and contact details
- Purpose of processing (marketing)
- Legal basis (consent or legitimate interest)
- How long you'll keep their data
- Their rights (access, deletion, etc.)
- How to withdraw consent

**Include in:** Privacy policy, signup form, confirmation email

### Right to Withdraw Consent

**Requirements:**
- As easy to withdraw as it was to give
- One-click unsubscribe preferred
- Cannot make them log in to unsubscribe
- Cannot charge a fee
- Must be honored immediately

### Right of Access

**If requested, provide:**
- Confirmation you process their data
- Copy of their data
- Information about processing

**Response time:** Within 1 month (extendable to 3 months for complex requests)

### Right to Erasure ("Right to Be Forgotten")

**Upon request:**
- Delete their email and associated data
- Remove from all lists
- Confirm deletion

**Exceptions:**
- May keep minimal data to maintain suppression list
- Legal obligations to retain certain records

### Right to Data Portability

**If requested:**
- Provide their data in machine-readable format (CSV, JSON)
- Allow them to transfer to another service

---

## Email Content Requirements

### Every Marketing Email Must Include:

1. **Your Identity**
   - Company name
   - Physical address
   - Contact information

2. **Unsubscribe Link**
   - Clear and prominent
   - Works without login
   - One-click if possible

3. **Privacy Information**
   - Link to privacy policy
   - Or summary of key information

### Email Footer Template

```
---

[COMPANY NAME]
[Address Line 1]
[City, Postal Code, Country]

You received this email because you subscribed to [LIST NAME]
on [DATE] via [METHOD].

[Unsubscribe] | [Update Preferences] | [Privacy Policy]

Questions? Contact us at [EMAIL] or reply to this email.

© [YEAR] [COMPANY NAME]
```

---

## Special Considerations

### Existing Lists (Pre-GDPR)

If you have email lists from before GDPR:

**Option 1: Re-consent Campaign**
- Send email requesting explicit consent
- Only keep those who actively re-consent
- Delete the rest

**Option 2: Document Legitimate Interest**
- Conduct Legitimate Interest Assessment
- Document thoroughly
- Provide easy opt-out

**Recommended:** Re-consent for cleaner compliance

### Purchased or Third-Party Lists

**Generally NOT compliant with GDPR because:**
- Individuals didn't consent to YOUR marketing
- Consent is not transferable
- You cannot demonstrate valid consent

**Alternatives:**
- Co-marketing with consent at collection
- Lead generation with clear disclosure
- Advertising to reach new audiences

### B2B Email Marketing

**Slightly different rules in some cases:**
- Email Preference Service (ePrivacy Directive)
- Business contact information
- Legitimate interest may apply more broadly

**Still required:**
- Legal basis for processing
- Right to object
- Clear identification
- Unsubscribe mechanism

**Best practice:** Same standards as B2C

---

## ePrivacy Directive (Cookie Law)

The ePrivacy Directive works alongside GDPR for electronic communications.

**Key Points:**
- Applies to use of cookies and similar technologies
- Applies to electronic marketing
- Being replaced by ePrivacy Regulation (pending)

**For email marketing:**
- Tracking pixels may require consent
- Open/click tracking should be disclosed
- Consider impact on your email analytics

---

## Compliance Checklist

### Before Sending Marketing Emails

- [ ] Have documented consent (or legitimate interest assessment)
- [ ] Consent was freely given, specific, informed, and unambiguous
- [ ] Can prove when and how consent was obtained
- [ ] Privacy policy is up to date and accessible
- [ ] Have process for handling data subject requests

### Every Marketing Email

- [ ] Clear sender identification
- [ ] Physical address included
- [ ] Prominent unsubscribe link
- [ ] Link to privacy policy
- [ ] Clear that it's marketing content

### Ongoing Compliance

- [ ] Process unsubscribes immediately
- [ ] Maintain suppression list
- [ ] Respond to data requests within 1 month
- [ ] Keep consent records up to date
- [ ] Review and update consent mechanisms regularly
- [ ] Train staff on GDPR requirements

---

## Data Retention

### How Long to Keep Email Data

**Active subscribers:**
- As long as consent is valid and they remain engaged
- Consider re-consent after extended inactivity (e.g., 2 years)

**Unsubscribed contacts:**
- Keep on suppression list indefinitely (to prevent re-emailing)
- Delete other data per your retention policy

**Consent records:**
- Keep as long as you might need to demonstrate compliance
- Typically 3-7 years after last contact

### Retention Policy Example

| Data Type | Retention Period |
|-----------|------------------|
| Active subscriber data | Until unsubscribe + suppression |
| Consent records | 7 years after last email |
| Email engagement data | 2 years |
| Suppression list | Indefinite |
| Data subject request records | 7 years |

---

## Breach Notification

If email data is breached:

**Supervisory Authority:**
- Notify within 72 hours (if risk to individuals)
- Document the breach regardless

**Affected Individuals:**
- Notify without undue delay (if high risk)
- Explain what happened
- Explain what you're doing about it
- Provide contact for more information

---

## International Transfers

If transferring EU data outside the EU/EEA:

**Adequate Countries:**
- Some countries have adequacy decisions (e.g., UK, Canada for commercial data)
- Transfer freely as within EU

**Other Countries (including US):**
- Standard Contractual Clauses (SCCs)
- EU-US Data Privacy Framework (if certified)
- Binding Corporate Rules (for intra-company)

**For email service providers:**
- Ensure they have appropriate transfer mechanisms
- Check their GDPR compliance documentation

---

## Documentation Templates

### Consent Record Template

```
CONSENT RECORD

Subscriber: [EMAIL]
Date of Consent: [DATE/TIME]
Method: [Website form / Checkout / Event]
Form URL: [URL]
IP Address: [IP]

Consent Text Displayed:
"[EXACT TEXT SHOWN TO USER]"

Double Opt-In Confirmed: [DATE/TIME] / N/A
Status: Active / Unsubscribed / Deleted
Last Activity: [DATE]
```

### Legitimate Interest Assessment Template

```
LEGITIMATE INTEREST ASSESSMENT (LIA)

Date: [DATE]
Assessor: [NAME]
Processing Activity: Email marketing to existing customers

1. PURPOSE TEST
What is the legitimate interest?
[DESCRIBE]

Is it lawful?
[YES/NO + EXPLANATION]

2. NECESSITY TEST
Is this processing necessary for the purpose?
[YES/NO + EXPLANATION]

Could the purpose be achieved another way?
[EXPLANATION]

3. BALANCING TEST
What is the impact on individuals?
[DESCRIBE]

Would individuals expect this processing?
[YES/NO + EXPLANATION]

Are individuals vulnerable?
[YES/NO]

What safeguards are in place?
[LIST SAFEGUARDS: easy opt-out, clear disclosure, etc.]

CONCLUSION
Does the legitimate interest override individuals' rights?
[YES/NO + JUSTIFICATION]

Review Date: [DATE]
```

---

*This guide is provided for informational purposes only and does not constitute legal advice. GDPR is complex and enforcement approaches vary. Consult with a qualified attorney to ensure compliance.*
