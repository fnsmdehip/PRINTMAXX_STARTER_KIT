# PrayerLock PWA - Deployment Guide

All options below are free tier. Pick one.

## Option 1: Vercel (recommended)

Fastest. Automatic HTTPS. Global CDN.

```bash
# Install Vercel CLI (one time)
npm i -g vercel

# Deploy from the prayerlock-web directory
cd MONEY_METHODS/APP_FACTORY/builds/prayerlock-web
vercel deploy --prod
```

Custom domain: Vercel dashboard > Project > Settings > Domains > Add `prayerlock.app` (or whatever you buy).

## Option 2: Netlify

Drag and drop. No CLI needed.

1. Go to https://app.netlify.com/drop
2. Drag the entire `prayerlock-web` folder onto the page
3. Done. You get a `.netlify.app` URL instantly.

CLI alternative:
```bash
npm i -g netlify-cli
cd MONEY_METHODS/APP_FACTORY/builds/prayerlock-web
netlify deploy --prod --dir .
```

## Option 3: GitHub Pages

Free hosting tied to a repo.

```bash
# Create new repo
gh repo create prayerlock --public
cd MONEY_METHODS/APP_FACTORY/builds/prayerlock-web
git init
git add .
git commit -m "PrayerLock PWA v1.0.0"
git remote add origin https://github.com/YOUR_USERNAME/prayerlock.git
git push -u origin main
```

Then: Repo > Settings > Pages > Source: Deploy from branch > `main` > `/ (root)` > Save.

Live at `https://YOUR_USERNAME.github.io/prayerlock/`

## Option 4: Cloudflare Pages

Fast global edge network. Free SSL.

1. Push to GitHub (see Option 3)
2. Go to https://dash.cloudflare.com/ > Pages > Create project
3. Connect GitHub repo
4. Build command: leave blank (static files)
5. Output directory: `.`
6. Deploy

Custom domain: Cloudflare dashboard > Pages > Custom domains.

## Option 5: Surge.sh

One command deploy. No account needed first time.

```bash
npm i -g surge
cd MONEY_METHODS/APP_FACTORY/builds/prayerlock-web
surge . prayerlock.surge.sh
```

## After deploying

1. Test PWA install: Open site on phone > browser menu > "Add to Home Screen"
2. Test offline: Turn on airplane mode after first load. App should still work.
3. Run Lighthouse audit in Chrome DevTools > Lighthouse tab > check PWA
4. Submit to PWA directories:
   - https://www.pwa.rocks/
   - https://appsco.pe/
   - https://pwa-directory.appspot.com/

## Custom domain setup

Buy a domain ($8-12/year):
- Namecheap: `prayerlock.app` or `prayerlock.co`
- Cloudflare Registrar: cheapest renewals
- Google Domains (now Squarespace): `.app` domains

Point DNS to your hosting provider per their docs. All 4 options above support custom domains on free tier.
