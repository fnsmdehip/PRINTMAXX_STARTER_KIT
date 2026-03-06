# InvoiceForge - Deploy to Surge

## Quick Deploy

```bash
cd MONEY_METHODS/APP_FACTORY/builds/invoiceforge
npx surge . invoiceforge.surge.sh
```

## Custom Domain

```bash
npx surge . yourcustomdomain.com
```

## Files
- index.html - Full app (single file, all CSS+JS inline)
- manifest.json - PWA manifest
- sw.js - Service worker for offline support
- deploy.md - This file

## Notes
- No build step required. Static files only.
- Works offline after first visit.
- All data stored in localStorage on user device.
- PDF export uses window.print() (browser native).
- "Pay Now" button requires user to set their own Stripe payment link.
- No server, no API, no database.
