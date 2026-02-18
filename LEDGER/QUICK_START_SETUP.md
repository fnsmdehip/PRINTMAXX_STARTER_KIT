# PRINTMAXX Quick Start Setup

**Timeline:** 15-20 min total (not hours)
**Philosophy:** Brave for quick start → GoLogin + Decodo for scale → Playwright for automation

---

## Browser Strategy

| Phase | Browser | Purpose |
|-------|---------|---------|
| Quick Start | Brave | Fast account creation, no tracking |
| Multi-Account | GoLogin + Decodo | Anti-detect fingerprints, different IPs |
| Automation | Playwright/Selenium | Bulk operations, avoids LLM extension issues |

**Why not Chrome + extensions?** LLM browser extensions cause issues with automation. Use Playwright directly.

---

## STEP 1: Open Brave Browser (1 min)

Download if needed: https://brave.com

Use Brave for all initial signups. It's fast and blocks tracking.

---

## STEP 2: Services - All Tabs Open (2 min)

Open these tabs in Brave:

```
Tab 1: https://gologin.com (Free tier - download app)
Tab 2: https://app.decodo.com (Proxies - $50/mo) [PAYMENT]
Tab 3: https://smspool.net (Phone verification - $10) [PAYMENT]
Tab 4: https://protonmail.com/signup (Free emails)
Tab 5: https://x.com/i/flow/signup (Accounts)
Tab 6: https://gumroad.com (Products)
```

---

## STEP 3: GoLogin Setup (2 min)

1. Sign up free at gologin.com
2. Download desktop app
3. Create 5 browser profiles:
   - Profile1: Windows/Chrome
   - Profile2: Mac/Safari
   - Profile3: Linux/Firefox
   - Profile4: Android/Chrome Mobile
   - Profile5: iPhone/Safari Mobile

Don't connect proxies yet - do that after Decodo.

---

## STEP 4: Decodo Proxies (2 min) [PAYMENT REQUIRED]

1. Go to app.decodo.com
2. Sign up
3. Get 1GB Residential plan ($50/mo)
4. Download proxy config file
5. Add IPs to GoLogin profiles (1 IP per profile)

**Test:** Open whatismyip.com in each GoLogin profile - should show different IPs.

---

## STEP 5: SMSPool (2 min) [PAYMENT REQUIRED]

1. Sign up at smspool.net
2. Add $10 credit
3. Buy 5 US phone numbers ($0.50 each = $2.50)
4. Save numbers for account verification

---

## STEP 6: ProtonMail - 4 Emails (3 min)

Create in Brave (regular browser, not GoLogin):

| Email | Brand |
|-------|-------|
| printmaxxer@protonmail.com | Meta brand |
| stackpilot.ai@protonmail.com | AI niche |
| dailyanchor.co@protonmail.com | Faith niche |
| 3hourphysique@protonmail.com | Fitness niche |

---

## STEP 7: X Accounts (5 min)

Use GoLogin profiles + Decodo proxies + SMSPool numbers:

| Profile | Account | Email | Phone |
|---------|---------|-------|-------|
| Profile1 | @PRINTMAXXER | printmaxxer@ | Number1 |
| Profile2 | @StackPilotAI | stackpilot.ai@ | Number2 |
| Profile3 | @DailyAnchorHQ | dailyanchor.co@ | Number3 |
| Profile4 | @3HourPhysique | 3hourphysique@ | Number4 |

**Bio templates from:** LEDGER/BRANDED_ACCOUNTS.md

---

## STEP 8: Gumroad Products (3 min)

1. Sign up at gumroad.com with printmaxxer@protonmail.com
2. Create 3 products:

| Product | Price | Copy Source |
|---------|-------|-------------|
| AI Clarity Stack | $47 | PRODUCTS/gumroad_copy/ai_clarity_stack_gumroad.md |
| Daily Anchor System | $27 | PRODUCTS/gumroad_copy/daily_anchor_system_gumroad.md |
| 3-Hour Physique | $47 | PRODUCTS/gumroad_copy/three_hour_physique_gumroad.md |

---

## STEP 9: Warmup Start (Ongoing)

For each X account, daily for 7 days:

| Action | Count | Time |
|--------|-------|------|
| Follows | 15-20 | 5 min |
| Likes | 20-30 | 5 min |
| Replies | 3-5 | 10 min |
| Posting | NONE | - |

**Start posting after Day 7.**

---

## Optional: Skip Warmup

Buy pre-warmed accounts:
- AccsMarket: https://accsmarket.com
- Fameswap: https://fameswap.com

Cost: $20-50 per aged/warmed account

---

## Automation Stack (After Setup)

Once accounts exist, use Playwright for bulk operations:

```python
# AUTOMATIONS/ uses Playwright for:
- Content posting
- Engagement automation
- Data scraping
- Alpha extraction
```

**Why Playwright over browser extensions?**
- No LLM extension conflicts
- Faster execution
- Better reliability
- Runs headless for overnight jobs

---

## Total Cost

| Service | Cost |
|---------|------|
| GoLogin | $0 (free tier) |
| Decodo | $50/mo |
| SMSPool | $10 (one-time for numbers) |
| ProtonMail | $0 |
| X Accounts | $0 |
| Gumroad | $0 |
| **TOTAL** | **$60** |

---

## After Setup Complete

Run these agent commands:
```
/parallel-launch content  # Generate 50 longtail + 100 posts
/deploy-check             # Validate landing site
/daily-research           # Scan alpha sources
```

---

## Checklist

- [ ] Brave browser ready
- [ ] GoLogin app installed, 5 profiles created
- [ ] Decodo proxies active, connected to GoLogin
- [ ] SMSPool funded, 5 numbers purchased
- [ ] 4 ProtonMail emails created
- [ ] 4 X accounts created with bios
- [ ] 3 Gumroad products live
- [ ] Warmup started (Day 1)
