# Email Templates

Production-ready HTML email templates for the PRINTMAXX content system.

## Template inventory

| Template | Purpose | Status |
|----------|---------|--------|
| welcome_template.html | Welcome email with resource delivery | Ready |
| launch_announcement.html | Product launch with countdown and pricing | Ready |
| newsletter_weekly.html | Weekly digest with 3 content blocks | Ready |
| trial_expiring.html | Trial ending reminder with usage stats | Ready |
| receipt_template.html | Purchase confirmation with upsell | Ready |
| winback_template.html | Re-engagement with special offer | Ready |
| launch_template.html | Simple launch announcement | Ready |
| nurture_template.html | Educational nurture sequence | Ready |
| transactional_template.html | Generic transactional base | Ready |

## Preview screenshots

Screenshots should be added after testing in email clients.

| Template | Desktop | Mobile | Dark Mode |
|----------|---------|--------|-----------|
| welcome_template.html | [placeholder] | [placeholder] | [placeholder] |
| launch_announcement.html | [placeholder] | [placeholder] | [placeholder] |
| newsletter_weekly.html | [placeholder] | [placeholder] | [placeholder] |
| trial_expiring.html | [placeholder] | [placeholder] | [placeholder] |
| receipt_template.html | [placeholder] | [placeholder] | [placeholder] |
| winback_template.html | [placeholder] | [placeholder] | [placeholder] |

## Template specifications

All templates include:
- Inline CSS for email client compatibility
- Mobile responsive design (600px max width)
- Plain text fallback in HTML comments
- Web-safe fonts with system fallbacks
- Preheader text support
- MSO conditionals for Outlook compatibility
- Dark mode support via media queries
- Accessible markup with proper roles

## Personalization tokens

Common tokens used across templates:

### User data
- `{{first_name}}` - Recipient's first name
- `{{email}}` - Recipient's email address

### App/Company data
- `{{app_name}}` - Product name
- `{{company_name}}` - Company name
- `{{company_address}}` - Physical address (CAN-SPAM)
- `{{sender_name}}` - Sender's name

### URLs
- `{{cta_url}}` - Primary call-to-action link
- `{{unsubscribe_url}}` - Unsubscribe link (required)
- `{{preferences_url}}` - Email preferences page
- `{{twitter_url}}` - Twitter/X profile
- `{{instagram_url}}` - Instagram profile
- `{{youtube_url}}` - YouTube channel

### Styling
- `{{primary_color}}` - Brand primary color (hex)
- `{{primary_color_dark}}` - Darker variant for hover states
- `{{secondary_color}}` - Brand secondary color

## Testing checklist

Before sending:

- [ ] Test in Gmail (web and app)
- [ ] Test in Apple Mail
- [ ] Test in Outlook (desktop and web)
- [ ] Test in Yahoo Mail
- [ ] Verify all links work
- [ ] Check images load correctly
- [ ] Test with images disabled
- [ ] Verify mobile responsiveness
- [ ] Check dark mode rendering
- [ ] Validate preheader displays correctly
- [ ] Confirm unsubscribe link works
- [ ] Run through mail-tester.com for spam score

## Usage notes

### ESP integration

Templates use double-brace syntax `{{variable}}` which works with:
- ConvertKit
- Mailchimp (use `*|VARIABLE|*` syntax instead)
- Beehiiv
- Buttondown
- SendGrid

Adjust merge tag syntax for your specific ESP.

### Image hosting

Replace image placeholder URLs with:
1. CDN-hosted images (recommended)
2. ESP-hosted images
3. Direct links to public S3/Cloudflare R2

Avoid: hosting images on your own server (deliverability risk).

### File size

Keep total email size under 102KB to avoid Gmail clipping.

Current sizes:
- welcome_template.html: ~9KB
- launch_announcement.html: ~12KB
- newsletter_weekly.html: ~11KB
- trial_expiring.html: ~10KB
- receipt_template.html: ~12KB
- winback_template.html: ~11KB

## Brand-specific templates

### prayerlock/
Templates customized for PrayerLock (faith niche).

### walktounlock/
Templates customized for WalkToUnlock (fitness niche).

## Copy style reminders

Per copy-style.md:
- No em dashes
- No AI vocabulary (leverage, utilize, comprehensive, etc.)
- Direct, specific language
- Start with the conclusion
- One idea per sentence
