# Cloudflare Pages Migration — 5-Minute Quickstart

**Goal:** Move 6 highest-value pages from Surge.sh → Cloudflare Pages, unlock search indexing
**Estimated time:** 5 minutes
**Revenue impact:** $2-8K/month organic traffic potential

---

## Step 1: Sign up Cloudflare Pages (3 min)

1. Go to https://dash.cloudflare.com/sign-up
2. Create account (email + password)
3. Verify email
4. Skip to "Pages" section

---

## Step 2: Install wrangler CLI (2 min)

```bash
npm install -g wrangler
wrangler login  # Opens browser, approve
```

---

## Step 3: I handle the rest (automation)

Once wrangler is authenticated, run:

```bash
bash AUTOMATIONS/seo_platform_migration.sh --prepare && --deploy
```

**What this does:**
- Prepares 6 sites for Cloudflare
- Deploys in parallel (15 min total)
- Sets up auto-redirects from surge.sh
- Submits sitemaps to Google

---

## Deployment targets (auto-handled)

| Page | Old URL | New URL | Keywords | Vol |
|------|---------|---------|----------|-----|
| AI Detector | ai-slop-detector.surge.sh | ai-slop-detector.pages.dev | "ai content detector" | 22K/mo |
| Ramadan (SEASONAL) | ramadan-tracker.surge.sh | ramadan-tracker.pages.dev | "ramadan tracker app" | 18K/mo |
| Vibe Coding | vibe-coding-cheat-sheet.surge.sh | vibe-coding-cheat-sheet.pages.dev | "vibe coding" | 12K/mo |
| Cursor vs Claude | cursor-vs-claude-code.surge.sh | cursor-vs-claude-code.pages.dev | "cursor vs claude code" | 9.1K/mo |
| Freelance Calc | freelance-rate-calc.surge.sh | freelance-rate-calc.pages.dev | "freelance calculator" | 8.1K/mo |
| SEMrush vs Ahrefs | semrush-vs-ahrefs.surge.sh | semrush-vs-ahrefs.pages.dev | "semrush vs ahrefs" | 6.5K/mo |

**TOTAL:** 65.5K monthly searches, currently invisible

---

## Verify deployment

After migration script completes:

```bash
curl -I https://ai-slop-detector.pages.dev/robots.txt
# Should show: Allow: /
```

Compare to old:
```bash
curl -I https://ai-slop-detector.surge.sh/robots.txt
# Shows: Disallow: /
```

---

## Optional: Custom domains

Once sites are live on Cloudflare, you can:
1. Add custom domains (e.g., ai-detector.printmaxx.com)
2. Enable SSL (automatic)
3. Setup auto-redirects

Script handles this if domains are registered.

---

## Troubleshooting

**"wrangler login fails"**
- Restart terminal: `source ~/.zshrc`
- Retry: `wrangler login`

**"Deployment timeout"**
- Cloudflare is slow sometimes
- Check status: `wrangler pages project list`

**"DNS errors after migration"**
- Pages will give you a Cloudflare nameserver
- Point your domain registrar to it (if using custom domain)

---

## That's it

Once wrangler is authenticated, you're done. The automation handles everything else.

Total time: **5 minutes**
Revenue unlock: **$2-8K/month** in organic traffic potential
