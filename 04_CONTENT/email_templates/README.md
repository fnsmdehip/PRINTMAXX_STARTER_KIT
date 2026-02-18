# Email templates

Production-ready HTML email templates for all PRINTMAXX apps.

## Quick start

1. Pick the app folder that matches your brand
2. Choose the template type (welcome, launch, nurture, transactional)
3. Replace `{{variables}}` with your content
4. Test in major email clients before sending

## Template types

### welcome.html
First email after signup. Delivers promised resource, explains setup, sets expectations.

**Use for:** New user onboarding, lead magnet delivery

**Key variables:**
- `{{first_name}}` - User's first name
- `{{app_link}}` - Link to open the app
- `{{download_link}}` - Link to download resource
- `{{step_1}}`, `{{step_2}}`, `{{step_3}}` - Setup steps

### launch.html
Product announcement email. Features, benefits, social proof, CTA.

**Use for:** App launches, major feature releases, waitlist announcements

**Key variables:**
- `{{app_name}}` - Product name
- `{{app_description}}` - What it does in one sentence
- `{{problem_statement}}` - Pain point it solves
- `{{screenshot_url}}` - App screenshot image
- `{{download_url}}` - App store or signup link
- `{{trial_days}}` - Free trial length

### nurture.html
Weekly value email. Tips, lessons, resources. Minimal header for casual feel.

**Use for:** Weekly newsletters, tips, lessons learned, resource roundups

**Key variables:**
- `{{headline}}` - Email main point
- `{{main_content_paragraph_1}}` - First paragraph
- `{{insight_label}}`, `{{insight_content}}` - Highlight box content
- `{{tip_title}}`, `{{tip_content}}` - Optional tip box
- `{{cta_url}}`, `{{cta_text}}` - Optional text link CTA
- `{{ps_content}}` - P.S. line content

### transactional.html
Account-related emails. Receipts, password resets, verification codes, trial expiring.

**Use for:** Purchase confirmations, password resets, account alerts, subscription changes

**Key variables:**
- `{{status_text}}` - Badge text (Confirmed, Pending, etc.)
- `{{headline}}` - Main message
- `{{intro_text}}` - Brief explanation
- `{{detail_label_1-3}}`, `{{detail_value_1-3}}` - Transaction details
- `{{total_label}}`, `{{total_value}}` - Total row
- `{{cta_url}}`, `{{cta_text}}` - Action button

## Universal variables

These work across all templates:

```
{{first_name}} - Recipient's first name
{{sender_name}} - Your name or team name
{{company_name}} - Legal company name
{{company_address}} - Physical address (required by CAN-SPAM)
{{unsubscribe_url}} - One-click unsubscribe link
{{preferences_url}} - Email preferences page
{{twitter_url}} - Twitter/X profile
{{instagram_url}} - Instagram profile
{{preheader_text}} - Preview text shown in inbox
```

## App-specific templates

Each app has customized templates with brand colors and messaging:

| App | Colors | Theme |
|-----|--------|-------|
| prayerlock | Gold/Blue | Calming faith-focused |
| walktounlock | Green/White | Energetic fitness |
| studylock | Purple/White | Focused academic |
| promptvault | Blue/Purple | Tech productivity |
| dailyanchor | Orange/Gold | Warm mindfulness |
| femfit | Pink/Purple | Feminine wellness |

See `brand_colors.json` for exact hex codes and gradients.

## Using the universal templates

The root templates (`welcome_template.html`, etc.) are generic. To use:

1. Copy to your working directory
2. Find and replace color variables:
   - `{{primary_color}}` - Main brand color
   - `{{primary_color_dark}}` - Darker variant for hover states
   - `{{primary_color_light}}` - Lighter variant for backgrounds
   - `{{secondary_color}}` - Accent color
3. Update content variables

## Email client compatibility

All templates tested in:

**Desktop:**
- Apple Mail
- Outlook 2016+
- Gmail (web)
- Yahoo Mail

**Mobile:**
- iOS Mail
- Gmail (mobile)
- Outlook (mobile)

**Features:**
- Mobile responsive (600px breakpoint)
- Dark mode support (prefers-color-scheme)
- Outlook conditional comments for fixes
- Table-based layout for maximum compatibility

## Dark mode

Templates automatically adjust for dark mode using:

```css
@media (prefers-color-scheme: dark) {
  /* Dark mode overrides */
}
```

No user action needed. Colors shift to comfortable dark variants.

## Testing checklist

Before sending:

- [ ] Preview in Litmus or Email on Acid
- [ ] Test all links
- [ ] Check images load (with and without)
- [ ] Verify unsubscribe works
- [ ] Test on mobile devices
- [ ] Send test to Gmail, Outlook, Apple Mail
- [ ] Check preheader displays correctly
- [ ] Verify dark mode looks good

## Variable syntax

Templates use `{{variable_name}}` syntax compatible with:

- ConvertKit
- MailerLite
- Mailchimp
- SendGrid
- Postmark
- Resend

Adjust syntax for your ESP if needed (e.g., `{{ variable_name }}` for Jinja2).

## Preheader text

The hidden preheader text appears in inbox previews. Format:

```html
<div class="preheader">Your preheader text here &#847; &#847; &#847; ...</div>
```

The `&#847;` characters are invisible spacers that prevent email client from pulling in body text.

Keep preheaders under 100 characters for best display.

## Image handling

**Best practices:**
- Host images on CDN (not inline base64)
- Include `alt` text for accessibility
- Provide `width` and `height` attributes
- Use absolute URLs

**Placeholder images:**
Templates use `{{screenshot_url}}`, `{{logo_url}}` variables. Replace with hosted image URLs.

## Social icons

Icons use Simple Icons CDN with CSS filters for coloring:

```html
<img src="https://cdn.jsdelivr.net/npm/simple-icons@v9/icons/x.svg"
     style="filter: brightness(0) invert(1);">
```

This keeps templates self-contained without hosting icon files.

## Compliance notes

All templates include:
- Physical mailing address (CAN-SPAM requirement)
- Unsubscribe link (required)
- Clear sender identification

For transactional emails, include note that user can't unsubscribe from account-related messages.

## Customization tips

**Change button style:**
Modify `.cta-button` class. Rounded: `border-radius: 50px`. Square: `border-radius: 6px`.

**Add sections:**
Copy table row structure. Keep table-based layout for compatibility.

**Change fonts:**
System fonts are used for maximum compatibility. For custom fonts, use web-safe fallbacks.

**Adjust spacing:**
Modify padding values. Email clients handle margins inconsistently, use padding instead.

## File structure

```
email_templates/
├── welcome_template.html      # Universal welcome
├── launch_template.html       # Universal launch
├── nurture_template.html      # Universal nurture
├── transactional_template.html # Universal transactional
├── brand_colors.json          # All app color codes
├── README.md                  # This file
├── prayerlock/
│   ├── welcome.html
│   ├── launch.html
│   ├── nurture.html
│   └── transactional.html
├── walktounlock/
│   └── ...
├── studylock/
│   └── ...
├── promptvault/
│   └── ...
├── dailyanchor/
│   └── ...
└── femfit/
    └── ...
```

## Support

Questions about templates? Check `CONTENT/email_sequences/` for content guidance and `.claude/rules/copy-style.md` for voice guidelines.