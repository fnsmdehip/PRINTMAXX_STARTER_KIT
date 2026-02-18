# Unsubscribe Requirements Guide

**Proper Opt-Out Handling for Email Compliance**

**IMPORTANT:** This is a reference guide, not legal advice. Consult with a qualified attorney for specific compliance questions.

---

## Overview

Proper unsubscribe handling is required by:
- CAN-SPAM Act (US)
- GDPR (EU/EEA)
- CASL (Canada)
- Various other privacy laws worldwide

This guide covers requirements and best practices for compliant unsubscribe mechanisms.

---

## Legal Requirements Summary

| Regulation | Requirement | Timeline |
|------------|-------------|----------|
| CAN-SPAM | Process opt-outs | Within 10 business days |
| GDPR | Honor withdrawal of consent | Without undue delay |
| CASL | Process opt-outs | Within 10 business days |
| CCPA/CPRA | Honor opt-out requests | Reasonable time |

---

## Unsubscribe Mechanism Requirements

### Must Have

**1. Clear and Conspicuous Link**
- Easy to find (not hidden)
- Readable text size and color
- Clear language ("Unsubscribe," "Opt-out")

**2. Functional Mechanism**
- Link must work for at least 30 days after email sent
- Must be operational 24/7
- Should work on all devices

**3. Simple Process**
- One-click preferred (highly recommended as of 2024)
- Maximum one confirmation page
- No login required
- No fee to unsubscribe
- No personal information required beyond email

**4. Prompt Processing**
- Legal requirement: 10 business days (CAN-SPAM/CASL)
- Best practice: Immediate (within minutes)

### Must NOT Have

- Pre-checked "keep me subscribed" boxes
- Confusing opt-out/opt-in language
- Multi-step unsubscribe processes
- Password or login requirements
- Fees or charges
- Mandatory surveys (can offer optional)
- Threats or guilt-tripping language

---

## One-Click Unsubscribe (RFC 8058)

As of February 2024, Google and Yahoo require one-click unsubscribe for bulk senders.

### Technical Implementation

**List-Unsubscribe Header:**
```
List-Unsubscribe: <mailto:unsubscribe@[DOMAIN].com?subject=unsubscribe>,
                 <https://[DOMAIN].com/unsubscribe?id=UNIQUE_ID>
List-Unsubscribe-Post: List-Unsubscribe=One-Click
```

**How it works:**
1. Email client reads the header
2. Shows "Unsubscribe" button in interface
3. One click sends POST request to your server
4. Subscriber is immediately unsubscribed

**Benefits:**
- Better deliverability
- Fewer spam complaints
- Better user experience
- Required by major email providers

### ESP Support

Most email service providers support this:
- Mailchimp
- ConvertKit
- Klaviyo
- ActiveCampaign
- SendGrid
- Mailgun

Check your ESP's documentation for setup instructions.

---

## Unsubscribe Link Placement

### Standard Placement (Footer)

```
-------------------------------------------

[COMPANY NAME] | [ADDRESS]

You received this email because you subscribed on [DATE].

[Unsubscribe] | [Manage Preferences] | [Privacy Policy]

-------------------------------------------
```

### Recommended Practices

| Element | Recommendation |
|---------|----------------|
| Location | Footer, but visible |
| Font size | Same as surrounding text (minimum) |
| Color | Same color as other links |
| Wording | "Unsubscribe" is universally understood |
| Contrast | Must be readable against background |

### What NOT to Do

```
// TOO HIDDEN
<p style="font-size: 6px; color: #f0f0f0;">unsubscribe</p>

// TOO COMPLICATED
To unsubscribe, reply to this email with "UNSUBSCRIBE" in the subject line,
then click the link we'll send you, then verify your identity...

// GUILT TRIP
Are you sure you want to break our hearts? Click here to abandon us forever.
```

---

## Unsubscribe Landing Page

### One-Click Confirmation Page

After clicking unsubscribe, show a simple confirmation:

```
You've been unsubscribed

You will no longer receive marketing emails from [COMPANY NAME].

This may take up to 24 hours to fully process.

Changed your mind? [Resubscribe]

Questions? Contact us at [EMAIL]
```

### Preference Center Option

Offer alternatives to complete unsubscribe:

```
Email Preferences for [EMAIL]

[ ] Unsubscribe from all emails

OR customize your preferences:

[ ] Product updates (weekly)
[ ] Blog digest (weekly)
[ ] Special offers (occasional)
[ ] Company news (monthly)

[Save Preferences]
```

### What to Include on the Page

- [ ] Confirmation that request was received
- [ ] Email address being unsubscribed
- [ ] Timeline for processing
- [ ] Option to resubscribe
- [ ] Contact information for questions
- [ ] (Optional) Preference management options
- [ ] (Optional) Brief, non-pushy survey

### What NOT to Include

- [ ] Login requirement
- [ ] Mandatory survey
- [ ] Complicated multi-step process
- [ ] Guilt-inducing language
- [ ] Hidden "Stay Subscribed" default
- [ ] More marketing

---

## Processing Unsubscribe Requests

### Immediate Actions

1. **Add to suppression list** - Prevent future emails
2. **Remove from active lists** - Stop upcoming campaigns
3. **Log the request** - Document for compliance
4. **Send confirmation** - Optional but good practice

### Technical Implementation

**Suppression List:**
- Global suppression list takes priority over all other lists
- Sync across all email systems
- Keep indefinitely (never delete from suppression)

**Database Update:**
```
UPDATE subscribers
SET status = 'unsubscribed',
    unsubscribe_date = NOW(),
    unsubscribe_source = 'email_link'
WHERE email = 'user@example.com'
```

**Suppression List Entry:**
```
{
  "email": "user@example.com",
  "unsubscribed_date": "2024-01-15T10:30:00Z",
  "source": "email_link_campaign_123",
  "lists_removed_from": ["newsletter", "promotions"],
  "suppression_active": true
}
```

### Processing Timeline

| Action | Timeline |
|--------|----------|
| Add to suppression | Immediately (within minutes) |
| Stop scheduled emails | Before next scheduled send |
| Remove from lists | Same day |
| Full propagation | Within 24 hours |
| Legal deadline | 10 business days maximum |

---

## Handling Different Unsubscribe Scenarios

### Unsubscribe from Specific List

If you have multiple lists/types:

```
You've been unsubscribed from: [LIST NAME]

You'll still receive:
- Transactional emails (order confirmations, etc.)
- [OTHER LISTS STILL SUBSCRIBED TO]

To unsubscribe from all marketing emails: [Unsubscribe from All]
```

### Unsubscribe from All Marketing

```
You've been unsubscribed from all marketing emails.

You'll still receive transactional emails related to your account
or purchases (order confirmations, shipping updates, etc.).

These are required to provide our service and cannot be opted out.
```

### Unsubscribe + Delete Data (GDPR)

If combined with data deletion request:

```
You've been unsubscribed and your data deletion request has been received.

We will:
- Stop all marketing emails immediately
- Delete your personal data within 30 days
- Keep your email on our suppression list only (to ensure we never
  email you again)

Confirmation will be sent within 30 days.
```

---

## Suppression List Management

### What Is a Suppression List?

A list of email addresses that must never receive marketing emails, regardless of how they might otherwise appear on your lists.

### Sources of Suppression Entries

1. **Unsubscribe requests** - From email links
2. **Bounce backs** - Invalid addresses
3. **Spam complaints** - People marking as spam
4. **Manual requests** - Via contact form or email
5. **Legal requests** - GDPR deletion, etc.

### Suppression List Rules

**DO:**
- Keep suppression list forever
- Check against suppression before every send
- Sync suppression across all email systems
- Include reason for suppression
- Update immediately upon new suppressions

**DO NOT:**
- Delete email addresses from suppression list
- Allow re-subscription without explicit re-consent
- Import lists that might contain suppressed addresses
- Ignore suppression list for "important" emails

### Re-Subscription After Unsubscribe

If someone wants to resubscribe:

1. **Explicit new consent required**
   - They must actively opt in again
   - Cannot just remove from suppression

2. **Process:**
   - User visits signup form
   - Enters email address
   - Confirms via double opt-in
   - Remove from suppression only after confirmation
   - Log new consent with fresh timestamp

---

## Confirmation Emails

### Unsubscribe Confirmation Email

**Should you send one?**

**Pros:**
- Confirms the request was processed
- Provides resubscribe option
- Good customer service

**Cons:**
- Technically sending email to someone who unsubscribed
- Could be seen as harassment if not done well

**Best Practice:**
- Send ONE brief confirmation
- Purely transactional (no marketing)
- Immediate (within minutes of unsubscribe)

**Template:**

```
Subject: You've been unsubscribed

Hi,

This confirms that [EMAIL] has been unsubscribed from [COMPANY NAME]
marketing emails.

You won't receive marketing emails from us anymore.

Changed your mind? You can resubscribe anytime at [LINK].

If you didn't request this, please contact us at [EMAIL].

[COMPANY NAME]
[ADDRESS]
```

---

## Common Mistakes to Avoid

### Technical Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Broken unsubscribe links | CAN-SPAM violation | Test links regularly |
| Links expire too quickly | Must work 30+ days | Use permanent links |
| No suppression list sync | Re-send to unsubscribed | Sync across all systems |
| Slow processing | Violates 10-day rule | Automate immediately |

### Process Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Requiring login | Violates CAN-SPAM | One-click unsubscribe |
| Multi-step process | Frustrates users | Single confirmation page |
| Hidden link | Not "clear and conspicuous" | Visible placement |
| Only mailto: link | May not work for all | Web link as primary |

### Content Mistakes

| Mistake | Problem | Solution |
|---------|---------|----------|
| Guilt-trip language | Damages brand | Simple, neutral language |
| Mandatory surveys | Barrier to unsubscribe | Make optional |
| Marketing on unsubscribe page | Inappropriate | Minimal, helpful content |
| No confirmation | User uncertainty | Show clear confirmation |

---

## Testing Checklist

Before launching email campaigns, verify:

### Unsubscribe Link
- [ ] Link is visible in email footer
- [ ] Link is not obscured by styling
- [ ] Link works on desktop browsers
- [ ] Link works on mobile browsers
- [ ] Link works in email clients (Gmail, Outlook, Apple Mail)

### Unsubscribe Process
- [ ] One-click unsubscribe works
- [ ] No login required
- [ ] No personal information required
- [ ] Process completes within 24 hours
- [ ] Confirmation page displays correctly
- [ ] Email stops arriving after unsubscribe

### Technical
- [ ] List-Unsubscribe header is present
- [ ] Suppression list is updated
- [ ] Subscriber status changes in database
- [ ] Future campaigns exclude unsubscribed address
- [ ] Confirmation email sends (if used)

### Compliance
- [ ] Meets CAN-SPAM requirements
- [ ] Meets GDPR requirements (if applicable)
- [ ] Meets CASL requirements (if applicable)
- [ ] Records are maintained for auditing

---

## Metrics to Track

| Metric | What It Indicates | Action Threshold |
|--------|-------------------|------------------|
| Unsubscribe rate | List health, content relevance | > 0.5% per campaign |
| Time to process | Technical efficiency | > 1 hour |
| Failed unsubscribes | Technical issues | Any failures |
| Re-subscription rate | Win-back opportunity | < 5% indicates issue |
| Spam complaints | Content/frequency issues | > 0.1% per campaign |

---

*This guide is provided for informational purposes only and does not constitute legal advice. Regulations may change. Consult with a qualified attorney to ensure compliance.*
