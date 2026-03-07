STATUS: PENDING_REVIEW
PLATFORM: Dev.to
DATE: 2026-03-07
TAGS: webdev, deployment, javascript, tools

---

TITLE: I deployed 140+ websites for free using surge.sh — here's the entire stack

---

# I deployed 140+ websites for free using surge.sh — here's the entire stack

32 days. 140+ live sites. $0 in hosting.

That's not a flex. It's a system. Here's exactly how it works.

---

## why surge.sh

Most developers I know use Vercel, Netlify, or GitHub Pages for static hosting. All solid options. But none of them let you deploy unlimited projects with zero config from a single CLI command without eventually hitting a limit or a bill.

surge.sh does.

```
npm install --global surge
surge
```

That's the entire setup. Two commands. The second one prompts you for your email and a project name (or auto-generates one). Your site is live in 30 seconds.

Free tier limits:
- Unlimited projects
- Custom domains (yes, on the free tier)
- HTTPS
- No monthly bandwidth cap listed for personal use

The only real limit is that surge is static-only. No server-side rendering, no edge functions, no database. If your app needs any of that, surge isn't the right tool. For anything that's a flat HTML/CSS/JS output, it's hard to beat.

---

## the project structure

140+ sites sounds overwhelming. It's not, because almost none of them are built from scratch.

The stack is a factory model:

```
base-template/
  index.html
  styles.css
  app.js
  manifest.json
  service-worker.js

variants/
  denomination-apps/    # 14 faith-specific PWAs
  local-biz-demos/      # 20+ city/business-type combos
  saas-tools/           # 5 tools
  landing-pages/        # product and service pages
```

Each variant starts from the same base template and gets its own:
- Color scheme (CSS custom properties, 3 lines to change)
- Content (denomination name, city name, business type)
- Manifest (app name, icons)
- Domain (auto-generated or custom)

A new denomination app takes about 8 minutes to spin up from the base template. A local biz demo takes 4.

---

## the deploy pipeline

Every project deploys with one command:

```bash
surge ./project-folder projectname.surge.sh
```

For batch deploys, I run a shell loop:

```bash
for dir in ./variants/denomination-apps/*/; do
  name=$(basename "$dir")
  surge "$dir" "$name.surge.sh"
done
```

That deploys an entire category of sites in one pass. 14 denomination apps deploy in under 3 minutes total.

No CI/CD setup. No GitHub Actions. No build step unless the project needs one (some of the SaaS tools use a simple Vite build before deploy).

For the SaaS tools with a build step:

```bash
cd ./saas-tools/sitescore-pro
npm run build
surge ./dist sitescore-pro.surge.sh
```

Vite build takes 8-15 seconds per tool. Total deploy time for all 5 SaaS tools from scratch: under 4 minutes.

---

## the PWA architecture

The denomination apps and the SaaS tools are all PWAs. Here's the pattern I use for every one:

```html
<!-- index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#1a1a2e">
  <link rel="manifest" href="/manifest.json">
  <title>App Name</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div id="app"></div>
  <script src="app.js"></script>
  <script>
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/service-worker.js');
    }
  </script>
</body>
</html>
```

```json
// manifest.json
{
  "name": "App Full Name",
  "short_name": "ShortName",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#1a1a2e",
  "theme_color": "#1a1a2e",
  "icons": [
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

```javascript
// service-worker.js
const CACHE_NAME = 'app-v1';
const ASSETS = ['/', '/styles.css', '/app.js', '/manifest.json'];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request))
  );
});
```

This gives every app offline capability, install-to-homescreen support, and a lighthouse PWA score above 90 with no additional configuration.

---

## the SaaS tools technical approach

The 5 SaaS tools do analysis client-side using Fetch API + DOMParser. No backend, no server costs, no API keys.

The core pattern for SiteScore and ShopMetrics:

```javascript
async function analyzeUrl(url) {
  const corsProxy = 'https://api.allorigins.win/get?url=';
  const response = await fetch(`${corsProxy}${encodeURIComponent(url)}`);
  const data = await response.json();
  const parser = new DOMParser();
  const doc = parser.parseFromString(data.contents, 'text/html');

  return {
    title: doc.querySelector('title')?.textContent || '',
    metaDescription: doc.querySelector('meta[name="description"]')?.content || '',
    h1Count: doc.querySelectorAll('h1').length,
    imageCount: doc.querySelectorAll('img').length,
    imagesWithoutAlt: doc.querySelectorAll('img:not([alt])').length,
    scriptCount: doc.querySelectorAll('script[src]').length,
    hasCanonical: !!doc.querySelector('link[rel="canonical"]'),
    hasOgTitle: !!doc.querySelector('meta[property="og:title"]'),
    hasTwitterCard: !!doc.querySelector('meta[name="twitter:card"]'),
    hasViewport: !!doc.querySelector('meta[name="viewport"]'),
    // ... 37 more signals
  };
}
```

The cold email calculator is pure JavaScript math with no external dependencies:

```javascript
function calculateRoi({ listSize, sendVolume, replyRate, closeRate, dealSize, toolCost }) {
  const sends = Math.min(sendVolume, listSize);
  const replies = Math.round(sends * (replyRate / 100));
  const closes = Math.round(replies * (closeRate / 100));
  const revenue = closes * dealSize;
  const roi = ((revenue - toolCost) / toolCost) * 100;
  return { sends, replies, closes, revenue, roi };
}
```

No backend means $0 running cost and no attack surface to maintain.

---

## the numbers

Sites deployed: 140+
Denomination PWAs: 14
Local biz demos: 20+ (8 cities, 4+ business types each)
SaaS tools: 5
Monthly hosting cost: $0
Deploy time per site (from template): 4-8 minutes
Batch deploy time (full category): under 4 minutes for 14 sites

The only money I spent was time. The surge.sh free tier handled everything.

---

## what surge.sh doesn't do

Worth being honest about the tradeoffs:

- No server-side rendering. React/Next.js apps need to be statically exported before deploying.
- No edge functions. Any dynamic logic runs in the browser.
- No built-in analytics. Add your own (I use a self-hosted Plausible snippet on most projects).
- No form handling. Use a third-party service (Formspree, Web3Forms) or redirect to a Typeform.
- No environment variables at runtime. Anything sensitive has to stay server-side, which means surge isn't the right tool for apps that need secrets in production.

For the 140+ projects in this sprint, none of those constraints were blockers. Static + client-side does everything I needed.

---

## the live tools

All of these are running on surge.sh free tier right now:

- shopmetrics-pro.surge.sh — Shopify store analyzer
- sitescore-free.surge.sh — 5-point site score
- sitescore-pro.surge.sh — 47-point full audit
- cold-email-calc.surge.sh — Cold email ROI calculator
- pagescorer.surge.sh — Free page scorer
- printmaxx-store.surge.sh — Digital product storefront
- printmaxx-digital-services.surge.sh — Service offerings
- printmaxx-flowstack.surge.sh — Workflow tool

All fast. All free. All deployable in under 30 seconds if I need to push an update.

If you're paying for static hosting and you're not at scale yet, try surge. The 30-second install is not an exaggeration.

---

## the actual lesson

The constraint of $0 hosting didn't limit what I built. It changed how I built it.

When hosting costs nothing, you stop treating sites as precious. You ship fast. You duplicate templates instead of over-engineering base systems. You give things away because the marginal cost of one more site is 4 minutes and $0.

That changes the economics of everything downstream.

Free tool with zero hosting cost = pure inbound lead gen with no downside.

That's the real stack.
