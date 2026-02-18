# Intelligent Lead Qualification Engine - Plan

## Goal
Build a quant-level lead qualification system that takes 2.87M bulk leads, visits their websites, and scores them on aesthetic quality, SEO, AIO/GIO readiness, design modernity, business activity, and industry budget potential. Output: ranked, qualified leads ready for cold email outreach.

## Architecture

### 1. Lead Pre-Filter (fast, no HTTP)
- Filter to leads WITH websites (~85% = ~2.4M)
- Prioritize high-margin industries: dental, legal, HVAC, roofing, real estate (highest discretionary budgets)
- Industry budget weighting from lead_scoring_criteria.md economics table
- Deduplicate by domain (many locations = same website)

### 2. Website Analysis Engine (HTTP + headless browser)
- **HTTP-level signals** (fast, ~0.5s per site):
  - SSL, response time, page size, status codes
  - CMS detection (WordPress, Squarespace, Wix, etc.)
  - CSS framework detection (Bootstrap version, Tailwind, etc.)
  - Meta tags, schema markup, analytics
  - Copyright year freshness
  - Mobile viewport meta tag

- **HTML content analysis** (medium, ~1s per site):
  - Design age indicators (table layouts, inline styles, Flash references, old jQuery)
  - Modern design indicators (CSS Grid, Flexbox, responsive images, lazy loading)
  - Content freshness (dates, copyright year, blog posts)
  - Contact info completeness (phone, email, address, hours)
  - Social media presence
  - Review/testimonial widgets
  - Accessibility basics (alt tags, ARIA)

- **SEO analysis**:
  - Title tag quality (length, keyword presence)
  - Meta description (exists, length, quality)
  - H1/H2 structure
  - Image alt tags
  - Schema/structured data
  - Sitemap existence
  - robots.txt
  - Page speed indicators (inline CSS, render-blocking scripts)

- **AIO/GIO readiness** (AI Overview / Generative IO):
  - Structured data completeness
  - FAQ/Q&A content
  - Entity markup
  - Content depth vs thin content
  - E-E-A-T signals (about page, credentials, authorship)

- **Aesthetic scoring** (design quality):
  - Modern CSS features (CSS variables, Grid, Flexbox)
  - Image quality indicators (retina, WebP/AVIF, proper sizing)
  - Font loading (Google Fonts, custom fonts vs system fonts)
  - Color scheme sophistication (CSS custom properties, gradient usage)
  - Animation/interaction (transitions, scroll effects)
  - Layout modernity (no tables, responsive design, proper spacing)
  - Professional indicators (custom 404, favicon, loading states)

### 3. Business Activity Detection
- HTTP status (is site even up?)
- Last-Modified / freshness headers
- Copyright year currency
- Social media last post dates (if detectable)
- Google Business Profile signals (hours, reviews)
- Phone number validation (format check)

### 4. Unified Scoring (0-100, higher = better prospect)
- **Website Quality Score** (40 points):
  - Design modernity: 0-15
  - SEO quality: 0-10
  - AIO/GIO readiness: 0-5
  - Mobile responsiveness: 0-5
  - Performance: 0-5

- **Business Viability Score** (30 points):
  - Industry margin tier: 0-10
  - Appears active: 0-5
  - Contact completeness: 0-5
  - Location quality: 0-5
  - Reviews/reputation signals: 0-5

- **Conversion Likelihood Score** (30 points):
  - Website pain level (bad site = higher): 0-15
  - Budget indicator (industry + location): 0-10
  - Decision maker accessibility: 0-5

### 5. Output
- QUALIFIED_LEADS_RANKED.csv with full scoring breakdown
- Per-industry CSV files
- HOT_LEADS (score >= 70) ready for immediate cold email
- Integration with generate_cold_emails.py

## Execution Plan
1. Build intelligent_lead_qualifier.py (~800 lines)
2. Test on 50 leads from each category
3. Run on full dataset (batch processing with rate limiting)
4. Generate output files
5. Connect to cold email pipeline
