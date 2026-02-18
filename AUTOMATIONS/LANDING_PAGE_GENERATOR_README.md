# Bulk Landing Page Generator

Professional landing page generator for $500 website redesign service targeting local businesses.

## Features

- 15 pre-built category templates (dentist, plumber, restaurant, law firm, etc.)
- Modern, responsive design using Tailwind CSS
- Complete SEO optimization (title, meta, schema.org markup)
- Professional copy tailored to each business category
- Single-file HTML output (no build step required)
- Category-specific color schemes
- Mobile-first responsive design
- Fast loading (CDN-only, no heavy frameworks)

## Usage

### Single Business Mode

Generate a landing page for one business:

```bash
python3 AUTOMATIONS/bulk_landing_page_generator.py \
  --name "Joe's Plumbing" \
  --category "plumber" \
  --city "Austin TX" \
  --phone "(512) 555-1234" \
  --email "joe@joesplumbing.com" \
  --preview
```

### Bulk CSV Mode

Generate landing pages for multiple businesses from a CSV:

```bash
python3 AUTOMATIONS/bulk_landing_page_generator.py \
  --csv local_biz_prospects.csv
```

**CSV Format:**
```csv
business_name,category,city,phone,email,url
Smith Family Dentistry,dentist,Austin TX,(512) 555-1001,info@smithdental.com,
Mike's HVAC,hvac,Austin TX,(512) 555-1002,mike@mikeshvac.com,
```

### Preview Generated Pages

The `--preview` flag automatically opens the generated page in your browser:

```bash
python3 AUTOMATIONS/bulk_landing_page_generator.py \
  --name "Bella's Salon" \
  --category "salon" \
  --city "Austin TX" \
  --phone "(512) 555-1234" \
  --preview
```

## Available Categories (15 Templates)

Each category has professionally-written copy, service descriptions, and optimized color schemes:

1. **dentist** - Family dentistry, cleanings, cosmetic, implants
2. **plumber** - Emergency repairs, drain cleaning, water heaters
3. **electrician** - Electrical repairs, panel upgrades, lighting
4. **hvac** - AC repair, heating systems, installation
5. **restaurant** - Dine-in, takeout, catering, events
6. **law_firm** - Personal injury, family law, estate planning
7. **real_estate** - Buying, selling, investment properties
8. **salon** - Hair, nails, skincare, special events
9. **gym** - Personal training, group classes, nutrition
10. **auto_repair** - Oil changes, brakes, diagnostics, AC
11. **landscaping** - Lawn care, design, irrigation, tree care
12. **cleaning_service** - Residential, deep cleaning, commercial
13. **contractor** - Kitchen/bathroom remodeling, additions
14. **accountant** - Tax prep, bookkeeping, IRS representation
15. **chiropractor** - Adjustments, sports injury, massage therapy

Unknown categories will get a generic professional template.

## Output Structure

```
AUTOMATIONS/output/landing_pages/
├── index.html                      # Preview index of all pages
├── generation_log.csv              # Log of generated pages
├── joes-plumbing.html             # Individual business page
├── smith-family-dentistry.html    # Individual business page
└── ...
```

## What Each Landing Page Includes

### Navigation Bar
- Fixed header with business name
- Desktop menu (Services, About, Reviews, Contact)
- Call-to-action button (phone)

### Hero Section
- Category-specific tagline
- Professional subtitle
- Dual CTAs (Get Free Quote + Phone)
- Trust badges (5-star, licensed, location)

### Services Section (4 services per business)
- Category-specific service cards
- Professional descriptions
- Icon visuals
- CTA button

### About Section
- Why choose this business
- Professional about copy
- 3 key differentiators
- Image placeholder + stats badge

### Testimonials Section
- 3 testimonial cards
- 5-star ratings
- Customer name + location
- (Marked as placeholder for actual reviews)

### Contact Section
- Contact form (name, email, phone, message)
- Contact info (phone, email, location)
- Business hours
- Emergency service notice

### Footer
- Business info + description
- Quick links
- Service area
- Social media placeholders
- Copyright notice

## SEO Features

Each page includes:
- Optimized title tag: `{Business Name} | {Tagline} in {City}`
- Meta description with location and services
- Open Graph tags for social sharing
- Schema.org LocalBusiness structured data
- Semantic HTML5 markup
- Mobile-friendly responsive design

## Color Schemes

Each category has a custom color palette:
- **Blue**: Dentist, Law Firm, Auto Repair, Accountant
- **Red**: Plumber, Restaurant
- **Orange**: Electrician, Contractor
- **Green**: HVAC, Gym, Landscaping
- **Cyan**: Cleaning Service
- **Purple**: Real Estate, Chiropractor
- **Pink**: Salon

## Integration with Cold Outbound

This tool pairs perfectly with the cold outbound lead gen system:

1. **Scrape local businesses** using local_biz_scraper.py
2. **Generate landing pages** for prospects using this tool
3. **Send cold email** with link to preview: "I built a modern website for you"
4. **Close deal** - they see the preview, you've already done 80% of the work

## Sales Process

```
Prospect Scraping
    ↓
Generate Preview Page (this tool)
    ↓
Cold Email with Preview Link
    ↓
"I already built your new site. Want to see it?"
    ↓
Close $500 Deal
    ↓
Minor customizations + go live
```

## Customization

To add new categories, edit `CATEGORY_TEMPLATES` in the script:

```python
"your_category": {
    "tagline": "Your Business Tagline",
    "hero_subtitle": "Compelling subtitle",
    "services": [
        {"name": "Service 1", "desc": "Description"},
        # ... 3 more services
    ],
    "about": "About paragraph",
    "colors": {"primary": "#HEX", "secondary": "#HEX", "accent": "#HEX"}
}
```

## Tips for $500 Website Service

1. **Generate preview BEFORE first contact** - show don't tell
2. **Use their actual business name** - personalization = higher conversion
3. **Include their real phone/email** - makes it feel complete
4. **Mark testimonials as placeholder** - FTC compliance
5. **Emphasize the value** - "I already built this for you"
6. **Offer minor customization** - photos, actual reviews, hours
7. **Bundle with basic SEO** - "I'll also set up Google Business Profile"

## Deployment

Generated pages are standalone HTML files that can be:
- Hosted on any web server (no build step)
- Uploaded to Netlify/Vercel (drag & drop)
- Served from S3/CloudFront
- Added to their existing hosting

## Next Steps

1. Integrate with `local_biz_scraper.py` to build automated pipeline
2. Connect to cold email system for outreach
3. Build portfolio site showing examples
4. Add "request changes" form for customization requests
5. Create video walkthrough for higher close rates

## Example Output

View sample output: `AUTOMATIONS/output/landing_pages/index.html`

---

**Built for the $500 website redesign cold outbound method.**
