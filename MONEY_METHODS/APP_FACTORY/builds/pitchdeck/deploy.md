# PitchDeck - Deploy to Surge

## Quick Deploy

```bash
cd MONEY_METHODS/APP_FACTORY/builds/pitchdeck
npx surge . pitchdeck.surge.sh
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

## Dependencies
- html2canvas loaded from CDN for slide image export
- Inter font from Google Fonts

## Notes
- No build step required. Static files only.
- Works offline after first visit (html2canvas cached by SW).
- All data stored in localStorage on user device.
- No server, no API, no database.
