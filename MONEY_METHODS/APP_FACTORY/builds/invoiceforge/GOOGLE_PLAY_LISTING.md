# InvoiceForge — Google Play Listing

## App Name (50 chars max)
InvoiceForge: Invoice Generator

## Short Description (80 chars max)
Professional invoices in 60 seconds. Built for tradespeople & freelancers.

## Full Description (4000 chars max)

**Make professional invoices in 60 seconds. Built for plumbers, electricians, HVAC techs, contractors, and freelancers.**

Stop losing money to slow invoicing. InvoiceForge lets you build a complete invoice on your phone, export it as a PDF, and send it before you even leave the job site.

**BUILT FOR TRADESPEOPLE**

Most invoice apps were designed for accountants. InvoiceForge was designed for the person on the roof, under the sink, or wiring a panel. Fast, no-nonsense, and built for how you actually work.

**FEATURES**

✓ Create invoices in under 60 seconds
✓ Trade-specific templates: Plumbing, Electrical, HVAC, Contractor, Landscaping, Cleaning, Freelance
✓ Auto-calculate line item totals, subtotals, and tax
✓ PDF export using Android's built-in PDF functionality
✓ Add your logo, business name, and payment terms
✓ Save client info for repeat jobs
✓ Add a payment link (Stripe, PayPal, Venmo — your choice)
✓ Track paid, pending, and overdue invoices
✓ Works completely offline — no internet needed

**PRIVATE BY DEFAULT**

All invoice data stays on your device. Zero data sent to any server. No account needed. No cloud storage.

**FREE TO START**

Create unlimited invoices. Export unlimited PDFs. No free tier limits.

---

**WHO USES IT**

• Plumbers, electricians, HVAC technicians
• General contractors and handymen
• Landscapers and lawn care
• House cleaners and maids
• Freelancers and consultants

---

Install it. Open it. Invoice in 60 seconds.

## Category
Business

## Content Rating
Everyone

## Tags
invoice, invoicing, billing, PDF, contractor, freelance, tradespeople, estimate, receipt

## Price
Free

## In-App Purchases
None at launch

## Privacy Policy URL
https://invoiceforge.surge.sh/privacy-policy.html

## App Icon
- 512x512px PNG, 32-bit with alpha
- Use icon-1024.svg as source — export at 512x512

## Feature Graphic (required)
- 1024x500px PNG/JPG
- Design: Dark background (#0c0c18), InvoiceForge in large white text, a mock invoice screenshot on the right, tagline "Invoices in 60 seconds" in emerald green

## Screenshots Required (phone: 1080x1920 or 1440x2560)
1. Invoice creation screen with trade template
2. Line items with auto-calculated totals
3. PDF preview screen
4. Invoice history / tracking screen
5. Client saved info screen

## Submission Method
**Option A (Recommended): TWA (Trusted Web Activity)**
- Deploy app to https://invoiceforge.surge.sh (already deployed or ready)
- Use Bubblewrap CLI: `npx @bubblewrap/cli init --manifest https://invoiceforge.surge.sh/manifest.json`
- Build APK: `bubblewrap build`
- Sign and upload to Play Console
- Fastest path to Play Store without writing native code

**Option B: Capacitor wrap**
- `npm install @capacitor/core @capacitor/cli`
- `npx cap init InvoiceForge io.printmaxx.invoiceforge`
- Add android platform, configure, build in Android Studio

## TWA Requirements Checklist
- [ ] App deployed to HTTPS URL
- [ ] manifest.json has valid icons (PNG files required — convert icon-1024.svg to PNG)
- [ ] Digital Asset Links file at /.well-known/assetlinks.json
- [ ] Bubblewrap CLI installed
