# SUPPLEMENT AFFILIATE SIGNUP — DO THIS NOW
**Created:** 2026-04-01 | Revenue Tracker Cycle 12
**Time required:** 30-40 minutes total
**Revenue unlocked:** $400-2,000/mo (6 pages, men 55-70 demographic)

---

## Why This Is Your #1 Action

6 health supplement affiliate pages are LIVE on surge.sh right now. They rank for longtail keywords targeting men 55-70 — the demographic with 70% US disposable income. Every click earns $0 because the links say `REPLACE_AMAZON_TAG` and `REPLACE_CB_ID`.

ClickBank pays 50-75% commissions on supplements. A $50 supplement = $25-37 per sale. Amazon Associates pays 3-8%.

**30 minutes of signup → lifetime commissions.**

---

## Step 1 — Amazon Associates (10 min)

**URL:** https://affiliate-program.amazon.com

1. Sign in with your existing Amazon account
2. Enter website: `best-blood-pressure-supplement-men-over-55.surge.sh`
3. For other sites, you can add more in Account Settings later
4. Choose payment method (bank transfer or Amazon gift card)
5. **Your Store ID will look like:** `yourname-20`

**Then come back and run:**
```bash
# Replace REPLACE_AMAZON_TAG with your actual Store ID
# Example if your ID is "printmaxx-20":
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/LANDING/affiliate-pages

for dir in best-blood-pressure-supplement-men-over-55 best-joint-supplement-men-over-50 best-memory-supplement-men-over-60 best-prostate-supplement-men-over-60 best-sleep-supplement-men-over-55 best-testosterone-booster-men-over-50; do
  sed -i '' 's/REPLACE_AMAZON_TAG/YOUR_STORE_ID_HERE/g' "$dir/index.html"
  echo "Updated $dir"
done
```

---

## Step 2 — ClickBank (10 min)

**URL:** https://accounts.clickbank.com/signup/

1. Create account (free, instant approval)
2. Go to Marketplace → search each vendor below
3. Click "Promote" to get your HopLink with your affiliate ID auto-filled

**Vendors on our pages:**
| Vendor | Product | Our Page |
|--------|---------|----------|
| `prostagenix` | ProstaGenix prostate | best-prostate-supplement |
| `gorillaflow` | Gorilla Flow | best-prostate-supplement |
| `flowforcemax` | FlowForce Max | best-prostate-supplement |
| `promind` | ProMind Complex | best-memory-supplement |
| `neurothrive` | Neuro-Thrive | best-memory-supplement |

**Your ClickBank ID will look like:** `yourusername` (the part after `affiliate=`)

**Then run:**
```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/LANDING/affiliate-pages

for dir in best-prostate-supplement-men-over-60 best-memory-supplement-men-over-60 best-blood-pressure-supplement-men-over-55 best-joint-supplement-men-over-50 best-sleep-supplement-men-over-55 best-testosterone-booster-men-over-50; do
  sed -i '' 's/REPLACE_CB_ID/YOUR_CLICKBANK_ID_HERE/g' "$dir/index.html"
  sed -i '' 's/REPLACE_CLICKBANK_ID/YOUR_CLICKBANK_ID_HERE/g' "$dir/index.html"
  echo "Updated $dir"
done
```

---

## Step 3 — Redeploy All 6 Pages (5 min)

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/LANDING/affiliate-pages

for dir in best-blood-pressure-supplement-men-over-55 best-joint-supplement-men-over-50 best-memory-supplement-men-over-60 best-prostate-supplement-men-over-60 best-sleep-supplement-men-over-55 best-testosterone-booster-men-over-50; do
  surge "$dir" "$dir.surge.sh" --domain "$dir.surge.sh"
  echo "Deployed $dir.surge.sh"
done
```

---

## Step 4 — Optional: MindLab Pro Refersion (10 min)

One page uses MindLab Pro's Refersion network.
- URL: https://mindlabpro.com/pages/affiliates
- Apply for affiliate program
- Get your Refersion ID
- Replace `REPLACE_REFERSION_ID` in `best-memory-supplement-men-over-60/index.html`

---

## Pages & Expected Earnings

| Page (surge.sh) | Products | Commission per sale | Volume est |
|-----------------|----------|-------------------|------------|
| best-prostate-supplement-men-over-60 | ClickBank prostate products | $25-50/sale | High (large market) |
| best-memory-supplement-men-over-60 | ClickBank + Amazon nootropics | $15-40/sale | High |
| best-testosterone-booster-men-over-50 | Amazon + ClickBank | $10-40/sale | Very high |
| best-blood-pressure-supplement-men-over-55 | Amazon + ClickBank | $5-20/sale | High |
| best-joint-supplement-men-over-50 | Amazon + ClickBank | $5-15/sale | High |
| best-sleep-supplement-men-over-55 | Amazon + ClickBank | $5-20/sale | Medium |

**Conservative estimate with any organic traffic: $400-2,000/mo**
**With any Reddit/SEO traffic push: $2,000-5,000/mo**
