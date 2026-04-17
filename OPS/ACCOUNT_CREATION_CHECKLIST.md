# ACCOUNT CREATION CHECKLIST
Updated: 2026-04-17 | Day 58 at $0 | Every minute this stays undone = money burning

Do these in order. Each one unlocks the next revenue channel. Total: ~2-3 hours if you move fast.

---

## 1. SURGE.SH LOGIN FIX (5 min) -- unlocks 136 site updates

CLI is logged in as fnsmdehip@proton.me but 136 domains owned by printmaxxweb@gmail.com.
```
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
npx surge logout
npx surge login
```
Use: `printmaxxweb@gmail.com` when prompted.
Verify: `npx surge list` shows your domains.

---

## 2. GUMROAD (15-45 min) -- unlocks 18 products + 6 bundles

Go to: gumroad.com/signup. Connect Stripe (already live).
Upload products from `GUMROAD_INSTANT_UPLOAD/` -- listings pre-written.
Paste-ready listings: `DIGITAL_PRODUCTS/ready_to_sell/LISTING_*.md`
Speed: ~2 min per product (upload PDF, paste title + price + description).

---

## 3. WHOP (15 min) -- unlocks 8 products at lower fees (5.7% vs 10%)

Go to: whop.com/sell. Connect same Stripe account. List higher-ticket products ($27+) first.

---

## 4. FIVERR (20 min) -- unlocks freelance arbitrage ($500-2K/mo)

Go to: fiverr.com/join. Category: Programming & Tech > AI Services.
Pre-written gig descriptions: `MONEY_METHODS/FREELANCE/fiverr_gigs/`
Price LOW for first 5 reviews (50% discount), then raise.

---

## 5. UPWORK (15 min) -- unlocks higher-ticket freelance

Go to: upwork.com/signup. Profile: AI automation + web dev.
Template proposals: `MONEY_METHODS/FREELANCE/upwork_proposals/`

---

## 6. X/TWITTER FINALIZE (10 min) -- unlocks content distribution

@PRINTMAXXER exists. Upload banner (`MEDIA/generated_images/twitter_banner.png`), PFP (`twitter_pfp.png`), set bio from `CONTENT/social/TWITTER_PROFILE_SPEC.md`. Post first 3 tweets from `CONTENT/social/posting_queue/`. Keep logged in for scraper.

---

## 7. AFFILIATE SIGNUPS (30 min) -- unlocks $400-2K/mo

| Program | Commission | URL |
|---------|-----------|-----|
| SEMrush | $200/referral | semrush.com/partners |
| ConvertKit | 30% recurring | convertkit.com/affiliates |
| Beehiiv | 50% year 1 | beehiiv.com/referrals |
| Instantly.ai | 30% recurring | instantly.ai/affiliates |
| Smartlead | 20% lifetime | smartlead.ai/affiliate |

After signup: `python3 AUTOMATIONS/payment_integrator.py --replace-placeholders`
Full instructions: `OPS/AFFILIATE_LINK_SETUP.md`

---

## 8. TAILSCALE (5 min) -- unlocks mobile control

```
/opt/homebrew/bin/tailscale login
```
Install Tailscale on iPhone, same login. Dashboard at `http://100.x.x.x:9999`.

---

## 9. EMAIL INFRA (15-30 min) -- unlocks cold outreach

Buy a cheap domain ($10/yr) for cold email (never cold email from main domain).
Set up Zoho Mail (free) or Google Workspace ($6/mo). Connect to Instantly.ai.

---

## ALREADY DONE (crossed off)
- [x] Stripe -- LIVE, keys in .env
- [x] RevenueCat -- LIVE
- [x] AdMob -- LIVE (ca-app-pub-5277873663568466~6431629011)

## TOTAL: ~2-3 hours. Unlocks ALL revenue channels.
