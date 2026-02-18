# PRINTMAXX Legal Compliance Guide

Comprehensive compliance requirements for apps, marketing, and content operations.

**Applies to:** All PRINTMAXX properties (apps, websites, marketing, social accounts)

---

## Table of Contents

1. [Privacy Compliance](#1-privacy-compliance)
2. [App Store Compliance](#2-app-store-compliance)
3. [FTC Marketing Compliance](#3-ftc-marketing-compliance)
4. [Subscription Compliance](#4-subscription-compliance)
5. [Content & Copyright](#5-content--copyright)
6. [Email Compliance](#6-email-compliance)
7. [Templates & Checklists](#7-templates--checklists)
8. [International Considerations](#8-international-considerations)

---

## 1. Privacy Compliance

### Privacy Policy Requirements

**Every app and website MUST have a privacy policy that discloses:**

| Requirement | What to Include |
|-------------|-----------------|
| Data collected | List all data types (email, device ID, usage data, etc.) |
| Purpose | Why you collect each data type |
| Third parties | Who you share data with (analytics, ads, payment processors) |
| Retention | How long you keep data |
| User rights | How users can access/delete their data |
| Contact info | Email for privacy inquiries |
| Updates | How you'll notify of policy changes |

**Minimum elements for PRINTMAXX apps:**

```
1. What we collect:
   - Account info (email, name)
   - Usage data (app interactions, session duration)
   - Device info (device type, OS version)
   - [If applicable] Health data, location, etc.

2. Why we collect it:
   - Provide app functionality
   - Improve user experience
   - Send notifications (if enabled)
   - Analytics and crash reporting

3. Third parties:
   - RevenueCat (subscription management)
   - Firebase/Analytics (usage analytics)
   - Sentry/Crashlytics (crash reporting)

4. Your rights:
   - Access your data
   - Delete your account
   - Opt out of marketing
   - Data portability
```

### GDPR Compliance (EU Users)

**Required if you have ANY EU users:**

| Requirement | Implementation |
|-------------|----------------|
| Lawful basis | Document legal basis for each data type |
| Consent | Get explicit consent before collecting |
| Data minimization | Only collect what you need |
| Right to erasure | Must delete data within 30 days of request |
| Data portability | Provide data in machine-readable format |
| Privacy by design | Build privacy into the product |
| DPO | Data Protection Officer if processing at scale |
| Breach notification | Report breaches within 72 hours |

**GDPR-specific additions to privacy policy:**

```
For EU Users:
- Legal basis: Consent / Contract / Legitimate interest
- Data transfers: [If transferring outside EU, list mechanisms]
- Rights: Access, rectification, erasure, portability, object, restrict
- Complaints: Right to file complaint with supervisory authority
- Contact: privacy@[yourdomain].com
```

### CCPA Compliance (California Users)

**Required if:**
- Gross revenue > $25M, OR
- Buy/sell/share data of 100K+ consumers, OR
- 50%+ revenue from selling personal info

**CCPA requirements:**

| Requirement | Implementation |
|-------------|----------------|
| Notice at collection | Tell users what you collect before/at collection |
| Opt-out of sale | "Do Not Sell My Personal Information" link |
| Right to know | Respond to requests within 45 days |
| Right to delete | Delete data on request |
| Non-discrimination | Can't penalize users who exercise rights |

**Add to privacy policy:**

```
California Privacy Rights (CCPA):
- Right to know what personal info we collect
- Right to delete your personal info
- Right to opt-out of sale of personal info
- Right to non-discrimination for exercising rights

To exercise these rights: privacy@[yourdomain].com
```

### Cookie Consent

**Website requirements:**

| Region | Requirement |
|--------|-------------|
| EU (GDPR) | Prior consent required for non-essential cookies |
| California | Disclosure required, opt-out for sale |
| Global best practice | Cookie banner with accept/decline |

**Cookie banner template:**

```
We use cookies for:
- Essential: Site functionality (always on)
- Analytics: Understanding usage (optional)
- Marketing: Relevant ads (optional)

[Accept All] [Manage Preferences] [Reject Non-Essential]
```

### Data Retention Policy

| Data Type | Retention Period | Deletion Method |
|-----------|------------------|-----------------|
| Account data | Until deletion requested | Full deletion |
| Usage analytics | 26 months | Anonymization |
| Support tickets | 3 years | Deletion |
| Payment records | 7 years (tax) | Archive, then delete |
| Marketing consent | Until withdrawn | Immediate removal |

---

## 2. App Store Compliance

### Apple App Store Requirements

**Privacy Nutrition Labels (Required):**

When submitting to App Store, you MUST complete the App Privacy section:

| Label | Disclose if you... |
|-------|-------------------|
| Data Used to Track You | Use data for cross-app tracking |
| Data Linked to You | Collect data tied to user identity |
| Data Not Linked to You | Collect anonymous/aggregated data |

**Common data types to declare:**

```
Contact Info: Name, email, phone
Identifiers: User ID, device ID
Usage Data: Product interaction, advertising data
Diagnostics: Crash data, performance data
Financial Info: Payment info (if handling payments)
Health & Fitness: Health data, fitness data (if applicable)
```

**Apple Review Guidelines to follow:**

| Guideline | Requirement |
|-----------|-------------|
| 3.1.1 | In-app purchase for digital goods/services |
| 3.1.2(a) | Subscription requirements (see below) |
| 4.2 | App must be complete and functional |
| 5.1 | Privacy policy required |
| 5.1.1 | Data collection disclosure |
| 5.1.2 | Data use limitation |

**Apple subscription requirements:**

1. Clearly communicate what user gets
2. Show price and duration prominently
3. Explain auto-renewal terms
4. Provide easy cancellation instructions
5. Free trial must clearly state when billing begins

### Google Play Data Safety

**Data Safety section (Required):**

| Question | Your Answer |
|----------|-------------|
| Does your app collect user data? | Yes/No |
| Is all collected data encrypted in transit? | Must be Yes |
| Do you provide a way to delete data? | Should be Yes |
| Data types collected | List all (contact, location, etc.) |
| Data shared with third parties | List all |

**Google Play requirements:**

| Requirement | Details |
|-------------|---------|
| Privacy policy | Required and must be accessible |
| Data safety | Complete Data Safety form |
| Permissions | Request only necessary permissions |
| Target audience | Age-appropriate content |
| Subscription | Clear pricing and cancellation |

### Age Ratings

| Rating | Content Guidelines |
|--------|-------------------|
| 4+ (Apple) / Everyone (Google) | No objectionable content |
| 9+ / Everyone 10+ | Mild/infrequent content |
| 12+ / Teen | Frequent/intense content |
| 17+ / Mature | Adults only |

**For PRINTMAXX apps:**
- PrayerLock: 4+ / Everyone
- WalkToUnlock: 4+ / Everyone
- StudyLock: 4+ / Everyone
- Faith apps: 4+ / Everyone
- Fitness apps: 4+ / Everyone

### Health Data Special Requirements

**If your app collects health/fitness data (HealthKit, Google Fit):**

| Requirement | Implementation |
|-------------|----------------|
| Apple HealthKit | Separate privacy policy section |
| Google Fit | Comply with Google Fit API Terms |
| Usage limitation | Only use for app functionality |
| No advertising | Cannot use health data for ads |
| No third parties | Cannot share with third parties |
| User consent | Explicit opt-in required |

---

## 3. FTC Marketing Compliance

### Affiliate Disclosure Requirements

**FTC requires "clear and conspicuous" disclosure:**

| Placement | Acceptable? |
|-----------|-------------|
| Beginning of post | YES - Recommended |
| Before affiliate link | YES |
| In video (verbal + text) | YES |
| End of post | NO - Too late |
| Buried in hashtags | NO |
| Only in bio | NO - Not sufficient |
| Small text/fine print | NO |

**Approved disclosure language:**

```
Short: "Affiliate link - I may earn commission"

Standard: "This post contains affiliate links. If you purchase
through these links, I may earn a commission at no extra cost to you."

Video: "This video contains affiliate links in the description.
I may earn a commission if you purchase."
```

**Platform-specific requirements:**

| Platform | Disclosure Method |
|----------|-------------------|
| TikTok | Verbal + text overlay, or branded content toggle |
| Instagram | Verbal + caption, or Paid Partnership label |
| YouTube | Verbal + paid promotion checkbox + description |
| Blog | Before first affiliate link |
| Email | Near affiliate links |

### Testimonial Requirements

**FTC Endorsement Guides:**

| Requirement | Details |
|-------------|---------|
| Truthful | Testimonials must reflect honest opinions |
| Typical results | If results aren't typical, must disclose |
| Material connection | Disclose if paid, received free product, etc. |
| Substantiation | Claims must be backed by evidence |

**Compliant testimonial format:**

```
"I lost 20 lbs using PrayerLock to build better habits."
- Sarah M., actual user

*Results may vary. Individual results depend on consistency and
other factors. Sarah received [free access/payment] for this review.
```

**Do NOT:**
- Use fake testimonials
- Generate testimonials with AI and present as real
- Cherry-pick extreme results without disclosure
- Claim "typical" results that aren't actually typical

### Income Claim Disclaimers

**CRITICAL: Any income/results claims require disclosure:**

**Required disclaimer for income claims:**

```
Results Disclaimer:
The income figures stated are not guarantees. Individual results
vary based on many factors including skill, dedication, market
conditions, and luck. Past performance does not guarantee future
results. We cannot and do not make any guarantees about your
ability to get results with our ideas, information, tools, or
strategies.
```

**Where to include:**
- Sales pages (near income claims)
- Email sequences (footer)
- Social posts making claims (in post)
- Testimonial pages (before testimonials)
- Course landing pages (prominent placement)

**Safe vs. Risky language:**

| Risky (Avoid) | Safe (Use) |
|---------------|------------|
| "Make $10K/month" | "Some users have reported earning..." |
| "Guaranteed results" | "Results vary based on..." |
| "You will earn..." | "Potential to earn..." |
| "Easy money" | "Requires consistent effort" |
| "Get rich quick" | "Build over time" |

### Comparative Advertising Rules

**When comparing to competitors:**

| Do | Don't |
|-----|-------|
| Use factual, verifiable claims | Make false statements about competitors |
| Compare like-to-like features | Cherry-pick unfair comparisons |
| Update comparisons regularly | Use outdated competitor info |
| Cite sources for claims | Make unsubstantiated claims |

---

## 4. Subscription Compliance

### Auto-Renewal Disclosure

**Required disclosures BEFORE purchase:**

```
Subscription Terms:
- Price: $X.XX per [week/month/year]
- Trial: [X days] free, then $X.XX/[period]
- Auto-renewal: Subscription automatically renews unless canceled
- Cancellation: Cancel anytime in Settings > Subscriptions
- Billing: Charged to [payment method] within 24 hours of period end
```

**Platform requirements:**

| Platform | Requirement |
|----------|-------------|
| Apple | Use StoreKit, show renewal terms |
| Google | Show price, period, auto-renewal |
| Web | Clear disclosure before payment |

### Free Trial Requirements

**What you MUST communicate:**

1. Trial duration (e.g., "7-day free trial")
2. What happens after trial ("Then $X.XX/month")
3. When billing starts ("After 7 days")
4. How to cancel ("Cancel anytime before trial ends")
5. Full price ("$59.99/year after trial")

**Compliant trial UI:**

```
[Button: Start 7-Day Free Trial]

Try premium free for 7 days. After your trial, you'll be
charged $4.99/month. Cancel anytime.
```

### Cancellation Requirements

**Make cancellation easy:**

| Requirement | Implementation |
|-------------|----------------|
| In-app instructions | Settings > Subscription > Cancel |
| Direct link | Link to device subscription settings |
| No dark patterns | Don't hide cancellation |
| Confirmation | Show cancellation was successful |
| Grace period | Allow cancellation before renewal |

**Required cancellation instructions:**

```
How to Cancel:
iOS: Settings > [Your Name] > Subscriptions > [App Name] > Cancel
Android: Play Store > Profile > Payments > Subscriptions > [App Name] > Cancel

Your subscription will remain active until the end of the current
billing period. You won't be charged again after cancellation.
```

### Refund Policy

**Template refund policy:**

```
Refund Policy:

Digital products are non-refundable once delivered/accessed.

For subscriptions:
- Apple App Store: Request refund through Apple
- Google Play: Request refund through Google Play

We may offer discretionary refunds for:
- Technical issues preventing access
- Duplicate charges
- Other circumstances at our discretion

Contact: support@[yourdomain].com
```

---

## 5. Content & Copyright

### Copyright Compliance

**Content you CAN use freely:**

| Source | License | Attribution Required? |
|--------|---------|----------------------|
| Your original content | N/A | No |
| Public domain | None | No (but good practice) |
| CC0 (Creative Commons Zero) | CC0 | No |
| CC BY | Creative Commons | Yes |
| Stock photos (paid) | License | Per license terms |

**Content that requires permission:**

| Content Type | Requirement |
|--------------|-------------|
| Music | License or royalty-free |
| Images | License or permission |
| Video clips | License or fair use (risky) |
| Quotes (short) | Fair use (likely OK) |
| Quotes (long) | Permission needed |
| Screenshots | Generally OK for review/commentary |

### DMCA Compliance

**If you host user content, you need:**

1. **DMCA Agent:** Registered with Copyright Office
2. **Takedown procedure:** Respond to valid requests
3. **Counter-notification:** Process for disputed claims
4. **Repeat infringer policy:** Terminate repeat offenders

**DMCA notice template (for receiving):**

```
To file a DMCA takedown notice, send to: dmca@[yourdomain].com

Include:
1. Identification of copyrighted work
2. Identification of infringing material
3. Contact information
4. Good faith statement
5. Accuracy statement
6. Physical or electronic signature
```

### User-Generated Content

**If users can submit content (reviews, posts, etc.):**

| Requirement | Implementation |
|-------------|----------------|
| Terms of service | Users grant you license to use |
| Content moderation | Remove illegal/infringing content |
| DMCA compliance | Takedown procedure |
| Report mechanism | Easy way to report violations |

**UGC license clause (for Terms of Service):**

```
User Content License:
By submitting content to [App/Service], you grant us a worldwide,
non-exclusive, royalty-free license to use, reproduce, modify,
and distribute your content in connection with our services.

You represent that you own or have rights to submit the content
and that it doesn't infringe any third-party rights.
```

### Trademark Guidelines

**Safe use of trademarks:**

| Use | OK? |
|-----|-----|
| Descriptive ("works with iPhone") | Yes |
| Comparative ("alternative to X") | Yes, if truthful |
| Logo use without permission | No |
| Implying endorsement | No |
| Domain names with trademarks | No |

---

## 6. Email Compliance

### CAN-SPAM Requirements (US)

**Every marketing email MUST include:**

| Requirement | Details |
|-------------|---------|
| From line | Accurate sender identification |
| Subject line | Not deceptive about content |
| Physical address | Valid postal address |
| Unsubscribe link | Working opt-out mechanism |
| Honor opt-outs | Within 10 business days |
| Identify as ad | If it's advertising |

**Compliant email footer:**

```
[Company Name]
[Physical Address]

You're receiving this because you signed up for [list/product].
[Unsubscribe] | [Update Preferences]
```

### GDPR Email Requirements (EU)

**Stricter than CAN-SPAM:**

| Requirement | Implementation |
|-------------|----------------|
| Prior consent | Opt-in required (no pre-checked boxes) |
| Specific consent | Separate consent for different lists |
| Proof of consent | Record when/how consent obtained |
| Easy withdrawal | One-click unsubscribe |
| Data access | Provide data on request |

**Double opt-in recommended:**
1. User enters email
2. Send confirmation email
3. User clicks to confirm
4. Added to list

### Transactional vs. Marketing Emails

| Type | Examples | Consent Required? |
|------|----------|-------------------|
| Transactional | Receipts, password reset, account updates | No |
| Marketing | Promotions, newsletters, upsells | Yes |
| Mixed | Transactional with marketing | Treat as marketing |

---

## 7. Templates & Checklists

### Privacy Policy Template

```markdown
# Privacy Policy

Last updated: [Date]

## Information We Collect

### Information You Provide
- Account information (email, name)
- [Other data types]

### Information Collected Automatically
- Device information
- Usage data
- [Other automatic data]

## How We Use Information

- Provide and improve our services
- Send notifications and updates
- Analyze usage patterns
- [Other uses]

## Information Sharing

We share information with:
- Service providers (analytics, payments)
- As required by law
- [Other sharing]

We do not sell your personal information.

## Your Rights

You may:
- Access your information
- Delete your account
- Opt out of marketing
- [Other rights based on jurisdiction]

## Data Security

We use industry-standard security measures including [encryption,
secure servers, etc.]

## Children's Privacy

Our services are not intended for children under 13. We do not
knowingly collect information from children under 13.

## Changes to This Policy

We may update this policy. We will notify you of material changes
by [email/in-app notification].

## Contact Us

privacy@[yourdomain].com
[Physical address]
```

### Terms of Service Template

```markdown
# Terms of Service

Last updated: [Date]

## Agreement to Terms

By using [App/Service], you agree to these Terms.

## Use of Service

You may use our service for lawful purposes only.

### Prohibited Uses
- Violate any laws
- Infringe intellectual property
- Transmit harmful code
- [Other prohibitions]

## Accounts

You are responsible for:
- Maintaining account security
- All activity under your account
- Providing accurate information

## Intellectual Property

[App/Service] and its content are owned by [Company].

## User Content

By submitting content, you grant us a license to use it.

## Subscriptions and Payments

[See pricing page for current prices]
- Subscriptions auto-renew unless cancelled
- No refunds for partial periods
- [Platform] handles payments

## Disclaimers

THE SERVICE IS PROVIDED "AS IS" WITHOUT WARRANTIES OF ANY KIND.

## Limitation of Liability

WE SHALL NOT BE LIABLE FOR ANY INDIRECT, INCIDENTAL, SPECIAL, OR
CONSEQUENTIAL DAMAGES.

## Governing Law

These Terms are governed by the laws of [State/Country].

## Changes to Terms

We may modify these Terms. Continued use constitutes acceptance.

## Contact

support@[yourdomain].com
```

### Pre-Launch Compliance Checklist

**For each new app/website:**

#### Legal Documents
- [ ] Privacy policy written and published
- [ ] Terms of service written and published
- [ ] Refund policy defined
- [ ] Cookie policy (if website with cookies)

#### App Store Compliance
- [ ] Privacy nutrition labels completed (Apple)
- [ ] Data safety section completed (Google)
- [ ] Age rating selected appropriately
- [ ] Subscription terms clearly displayed
- [ ] Auto-renewal disclosure included
- [ ] Cancellation instructions provided

#### Marketing Compliance
- [ ] Affiliate disclosures ready
- [ ] Testimonial disclaimers prepared
- [ ] Income claim disclaimers (if applicable)
- [ ] FTC-compliant disclosure language

#### Data Protection
- [ ] Data collection minimized
- [ ] Encryption in transit implemented
- [ ] Data deletion process defined
- [ ] GDPR compliance (if EU users expected)
- [ ] CCPA compliance (if CA users expected)

#### Email Setup
- [ ] Unsubscribe mechanism working
- [ ] Physical address in footer
- [ ] Sender name accurate
- [ ] Double opt-in implemented

### Monthly Compliance Audit

- [ ] Review privacy policy for accuracy
- [ ] Test unsubscribe links
- [ ] Check subscription cancellation flow
- [ ] Review recent marketing for disclosures
- [ ] Process any data deletion requests
- [ ] Update any outdated legal documents

---

## 8. International Considerations

### Jurisdiction Summary

| Jurisdiction | Key Laws | Priority |
|--------------|----------|----------|
| US (Federal) | FTC Act, CAN-SPAM, COPPA | HIGH |
| California | CCPA | HIGH |
| EU | GDPR, DSA | HIGH |
| UK | UK GDPR, DPA 2018 | MEDIUM |
| Canada | PIPEDA, CASL | MEDIUM |
| Australia | Privacy Act, Spam Act | LOW |

### Minimum Compliance Stack

**For global apps, implement:**

1. **Privacy policy** covering GDPR requirements (strictest)
2. **Cookie consent** for EU visitors
3. **Unsubscribe** for all marketing emails
4. **Data deletion** capability
5. **Clear disclosures** for marketing content

### When to Geo-Block

Consider blocking access from regions where:
- Compliance cost exceeds revenue potential
- You can't meet legal requirements
- Risk is too high

**Note:** Geo-blocking doesn't guarantee protection if users VPN.

---

## Quick Reference

### Minimum Viable Compliance

**Every PRINTMAXX property needs:**

1. Privacy policy URL
2. Terms of service URL
3. Affiliate disclosure template
4. Subscription terms (if applicable)
5. Results disclaimer (if income/results claims)
6. Contact email for inquiries

### Where to Host Legal Pages

| Option | Pros | Cons |
|--------|------|------|
| App website | SEO, easy updates | Need hosting |
| Notion | Free, easy | Less professional |
| Google Sites | Free, simple | Limited design |
| termly.io | Auto-generates | Monthly cost |
| iubenda | Auto-generates | Monthly cost |

### Legal Document Generators (Free/Low Cost)

| Service | What it generates | Cost |
|---------|-------------------|------|
| Termly | Privacy, Terms, Cookies | Free tier |
| iubenda | Privacy, Terms, Cookie | Free tier |
| GetTerms | Terms, Privacy | Free |
| PrivacyPolicies.com | Privacy policy | Free |
| Avodocs | Terms, Privacy | Free |

### When to Consult a Lawyer

- Before launch in regulated industry (health, finance)
- Receiving any legal notice
- Making specific income guarantees
- Collecting sensitive data (health, financial)
- Expanding to new markets with different laws
- Any uncertainty about compliance

---

## Update Log

| Date | Change |
|------|--------|
| 2026-01-25 | Initial document created |

---

## Sources & Further Reading

**Official Sources:**
- FTC Endorsement Guides: ftc.gov/endorsement-guides
- Apple App Store Guidelines: developer.apple.com/app-store/guidelines
- Google Play Policies: play.google.com/policy
- GDPR Official Text: gdpr-info.eu
- CCPA Official Text: oag.ca.gov/privacy/ccpa

**See Also:**
- `/MONEY_METHODS/APP_FACTORY/GREY_HAT_COMPLIANCE_PLAYBOOK.md` - Edge tactics
- `/OPS/MONETIZATION_PLAYBOOK.md` - Affiliate disclosure examples
- `/OPS/EMAIL_DELIVERABILITY_GUIDE.md` - CAN-SPAM compliance

---

*Disclaimer: This guide provides general information and is not legal advice.
Consult with a qualified attorney for specific legal questions.*
