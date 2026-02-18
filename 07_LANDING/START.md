# Quick Start Guide

## Running the Site Locally

From the repo root:

```bash
cd LANDING/printmaxx-site
npm run dev
```

The site will be available at `http://localhost:3000`

## Routes

- `/` - Homepage with lead capture
- `/truth` - Truth Pages index (10 pages)
- `/truth/[slug]` - Individual Truth Page
- `/magnet/stack-generator` - Stack Generator form

## Generating More Long-tail Pages

From the repo root:

```bash
# Generate next batch (modify script to change count)
python3 OPS/scripts/generate_longtail_pages.py
```

## Building for Production

```bash
cd LANDING/printmaxx-site
npm run build
npm start  # Run production server
```

## Deploying to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd LANDING/printmaxx-site
vercel
```

## Next Steps

1. Test the site locally
2. Review generated long-tail pages in `CONTENT/longtail_pages/`
3. Check lead capture works (test form → check `LEDGER/leads.csv`)
4. Deploy to Vercel when ready
5. Start daily posting (1 post + 10 replies on X)

## Notes

- Lead capture saves to `LEDGER/leads.csv`
- Truth pages load from `CONTENT/truth_pages/`
- All pages are statically generated at build time
- Site uses Tailwind CSS for styling
