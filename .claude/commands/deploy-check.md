---
name: deploy-check
description: Pre-flight deployment checklist for the landing site.
model: sonnet
---

# Deployment Checklist

Run pre-flight checks before deploying LANDING/printmaxx-site.

## Checks

1. **Build Test**
   - `cd LANDING/printmaxx-site && npm run build`
   - No TypeScript errors
   - No build warnings

2. **Environment Check**
   - .env.example exists
   - No secrets in committed files

3. **Performance Check**
   - Bundle size < 500KB gzipped
   - Images optimized
   - Lighthouse score > 90

4. **SEO Check**
   - All pages have meta titles
   - All pages have meta descriptions
   - Structured data present
   - sitemap.xml exists

5. **Compliance Check**
   - Privacy policy link works
   - Terms of service link works
   - FTC disclosures visible

## Output

- Pass/fail checklist
- Blocking issues (must fix)
- Warnings (should fix)
- Ready for deploy: YES/NO
