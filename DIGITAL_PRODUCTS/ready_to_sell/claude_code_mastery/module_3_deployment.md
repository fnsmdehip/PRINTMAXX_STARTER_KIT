# Module 3: Deploy to Production — Surge, Netlify, Vercel, Custom Domains

## What You'll Have After This Module

Your app live on the internet with a custom domain, SSL certificate, and automatic deployments. Three deployment options depending on what you need, each taking under 15 minutes.

## Option 1: Surge.sh — Fastest Path to Live (5 minutes)

Surge is the fastest way to get a static site live. No account creation. No dashboard. Just a terminal command.

### First Deploy

```bash
npm install -g surge
cd your-project-directory
surge ./ your-app-name.surge.sh
```

First time, it'll ask for an email and password. That creates your account. Every deploy after that is one command.

Your app is now live at `your-app-name.surge.sh`. Free. SSL included.

### Custom Domain on Surge

Buy a domain. Namecheap is cheapest at $8-12/year for a .com. Porkbun is $9/year and has free WHOIS privacy.

Add a CNAME file to your project root:

```bash
echo "myapp.com" > CNAME
```

In your domain registrar's DNS settings, add:

```
Type: CNAME
Host: @
Value: na-east1.surge.sh
```

For the www subdomain:

```
Type: CNAME
Host: www
Value: na-east1.surge.sh
```

Deploy again:

```bash
surge ./ myapp.com
```

DNS propagation takes 5-30 minutes. After that, `myapp.com` serves your app with automatic SSL.

### Surge Pricing

- Free tier: Unlimited projects, custom domains, SSL
- Surge Professional ($30/month): Password protection, CORS headers, custom redirects

For MVPs, free tier is all you need. Don't pay until you're making money.

### When to Use Surge

- Rapid prototyping (deploy in under 60 seconds)
- Static sites with no server-side logic
- When you want zero config and zero dashboard

## Option 2: Netlify — Best for Growing Apps (10 minutes)

Netlify adds features Surge doesn't have: form handling, serverless functions, branch deploys, and a visual dashboard.

### Setup

```bash
npm install -g netlify-cli
netlify login
```

This opens a browser window to authenticate. One-time setup.

### Deploy from Terminal

```bash
cd your-project-directory
netlify deploy --prod --dir .
```

First time, it'll ask you to create a new site or link to an existing one. Choose "Create & configure a new site."

Your app is live at `random-name-12345.netlify.app`.

### Custom Domain on Netlify

In the Netlify dashboard (app.netlify.com):

1. Go to your site > Domain settings > Add custom domain
2. Enter your domain (e.g., `myapp.com`)
3. Netlify gives you DNS records to add at your registrar

Option A — Use Netlify DNS (recommended):
- Change your domain's nameservers to Netlify's (they provide 4 nameservers)
- Everything's managed in one place
- Automatic SSL provisioning

Option B — External DNS:
- Add an A record pointing to `75.2.60.5`
- Add a CNAME for `www` pointing to your Netlify subdomain
- SSL still works but takes longer to provision

### Auto-Deploy from Git

This is where Netlify shines. Connect your GitHub repo:

```bash
cd your-project-directory
git init
git add -A
git commit -m "initial commit"
gh repo create myapp --public --push
netlify link
```

Now every `git push` automatically deploys your site. Branch deploys give you preview URLs for testing before merging.

### Netlify Functions (Serverless)

Need a backend endpoint? Create `netlify/functions/hello.js`:

```javascript
exports.handler = async (event) => {
  return {
    statusCode: 200,
    body: JSON.stringify({ message: "Hello from the backend" }),
  };
};
```

This is available at `/.netlify/functions/hello`. No server to manage. 125K free invocations/month.

Use this for: Stripe webhooks, email sending, API proxying (hide your API keys from the client).

### Netlify Pricing

- Free: 100GB bandwidth, 125K function invocations, 1 concurrent build
- Pro ($19/month): 1TB bandwidth, password protection, analytics
- You won't need Pro until you're past $500/month in revenue

### When to Use Netlify

- Apps that need serverless functions
- Team projects with branch deploys
- When you want form handling without a backend
- When git-based auto-deploy matters

## Option 3: Vercel — Best for Next.js and APIs (10 minutes)

Vercel is built by the Next.js team. If you're using Next.js, use Vercel. If you're using vanilla JS/HTML, Vercel still works but Surge or Netlify is simpler.

### Setup

```bash
npm install -g vercel
vercel login
```

### Deploy

```bash
cd your-project-directory
vercel --prod
```

First deploy asks a few questions (project name, framework, output directory). After that, `vercel --prod` is all you need.

### Custom Domain on Vercel

```bash
vercel domains add myapp.com
```

Vercel gives you DNS records. Add them at your registrar. Same process as Netlify — either use Vercel's nameservers or add A/CNAME records.

### Vercel Serverless Functions

Create `api/hello.js`:

```javascript
export default function handler(req, res) {
  res.status(200).json({ message: "Hello from Vercel" });
}
```

Available at `/api/hello`. Vercel's function syntax is simpler than Netlify's, and cold starts are faster.

### Edge Functions

Vercel's edge functions run at the CDN level — 50ms response times globally:

```javascript
// api/fast.js
export const config = { runtime: 'edge' };

export default function handler(req) {
  return new Response(JSON.stringify({ fast: true }), {
    headers: { 'content-type': 'application/json' },
  });
}
```

### Vercel Pricing

- Hobby (free): 100GB bandwidth, 100K function invocations
- Pro ($20/month): 1TB bandwidth, 1M invocations, team features
- Free tier is generous enough for apps making up to $1K/month

### When to Use Vercel

- Next.js projects (zero config, it just works)
- When you need edge functions for global speed
- API-heavy apps where every endpoint is a serverless function

## The Decision Matrix

| Need | Use |
|------|-----|
| Ship in 60 seconds, no account needed | Surge |
| Static site with custom domain | Surge |
| Need serverless functions | Netlify or Vercel |
| Git-based auto-deploy | Netlify or Vercel |
| Next.js app | Vercel |
| Form handling without backend | Netlify |
| Maximum simplicity | Surge |

## Domain Strategy for Multiple Apps

If you're shipping 10+ apps (Module 5), don't buy a domain for each one. That's $100+/year in domains alone.

Strategy: Buy one domain, use subdomains.

```
myapps.com         → portfolio/landing page
tracker.myapps.com → habit tracker
timer.myapps.com   → pomodoro app
split.myapps.com   → expense splitter
```

On Netlify/Vercel, each subdomain can point to a different project. One domain, unlimited apps.

Cost: $10/year for the domain. $0 for hosting. $0 for SSL.

## Post-Deploy Checklist

After every deploy, verify these five things:

1. **SSL works** — Visit `https://yourapp.com`. Green lock icon. No mixed content warnings.
2. **Mobile works** — Open on your phone. Test every interaction. Tap targets need to be 44x44px minimum.
3. **PWA installs** — On mobile Chrome, check if the "Add to Home Screen" prompt appears.
4. **Meta tags exist** — Open Graph tags for social sharing. Test with LinkedIn's Post Inspector and Twitter's Card Validator.
5. **Analytics tracking** — Add Plausible ($9/month, privacy-friendly) or Umami (free, self-hosted). You need data before you can optimize.

Add these OG tags to your `index.html`:

```html
<meta property="og:title" content="StreakPad — Build Better Habits">
<meta property="og:description" content="Track habits, build streaks, stay consistent. Free, offline, no account needed.">
<meta property="og:image" content="https://myapp.com/og-image.png">
<meta property="og:url" content="https://myapp.com">
<meta name="twitter:card" content="summary_large_image">
```

Create the OG image at 1200x630px. Use Figma (free) or tell Claude Code to generate an SVG and convert it.

## Deployment Automation

Once you've deployed manually 3 times, automate it. Add a deploy script to your `package.json`:

```json
{
  "scripts": {
    "deploy": "surge ./ myapp.com",
    "deploy:preview": "surge ./ preview-myapp.surge.sh"
  }
}
```

Now `npm run deploy` ships to production. `npm run deploy:preview` ships to a preview URL you can share for feedback.

Next module: Adding Stripe payments so your free app becomes a revenue-generating product.
