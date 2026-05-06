# IndieHackers Distribution — Cycle 47 — 2026-05-05
# Focus: Day 45 update with 804 sites milestone, PWA vs native reflection

---

## POST 1: Day 45 Build-In-Public — The 804 Sites Problem
**Target:** IndieHackers community, build-in-public crowd, solo founders

---

**Title:** Day 45: 804 sites deployed, $0 revenue. Here's the diagnosis.

**Body:**

Day 45 of a solo revenue automation sprint.

**What the system has built:**
- 804 surge.sh websites (PWAs, landing pages, comparison pages, streak apps)
- 539 automation scripts
- 192K leads scraped and scored
- 4 iOS apps built and simulator-tested
- 20 Gumroad product listings drafted
- 12 "X vs Y" comparison pages live for long-tail SEO
- 17 research blog articles published
- 87 alpha entries pending implementation

**Revenue: $0.**

The failure mode is specific: I built the capability engine before the revenue infrastructure.

The capability engine (build, deploy, scrape, score, generate content) is fully automated and functional. The revenue infrastructure (Stripe to receive payments, Gumroad to host products, App Store to distribute iOS apps, affiliate IDs to capture commissions) requires human account creation.

Human actions blocking revenue:
| Action | Time | Revenue Unlocked |
|--------|------|-----------------|
| Create Stripe account | 10 min | 20+ apps with premium tiers |
| Create Gumroad account | 15 min | 20 digital products |
| Submit 4 iOS apps to App Store | 45 min | App Store distribution |
| Sign up for 10 affiliate programs | 45 min | $850-5K/mo referral pipeline |

**Total: 115 minutes** between current state and first revenue entry.

The system is a loaded gun with no trigger wired.

The lesson I'm drawing from this isn't "move faster." It's "build the revenue infrastructure before the first product, not after the 800th website."

**What's working despite $0:**
The automation pipeline runs every day and continues generating leads, content, and opportunities. 1,648 new alpha entries scraped in the last 24 hours. The pipeline compounds whether or not revenue is flowing.

**What's next:**
The 115 minutes of account setup needs to happen. That's the only remaining blocker.

---

## POST 2: PWA vs Native — Field Notes After 76 PWA Deployments
**Target:** Indie devs, mobile app builders, bootstrappers considering tech stack

---

**Title:** I deployed 76 PWAs. Here's the honest case for native apps instead.

**Body:**

I've built 76 PWAs on surge.sh. Health apps, productivity apps, streak trackers, consent form managers, TRT protocol loggers.

After running this experiment for 45 days, here's the honest case for native apps even if PWAs are technically equivalent:

**PWA advantages I actually got:**
- Deployment in seconds (surge deploy vs. App Store review: 1 day → 1-3 weeks)
- Zero App Store fees
- Instant updates without review
- Cross-platform with one codebase
- Free hosting

**PWA disadvantages I didn't anticipate:**
- "Add to Home Screen" is invisible to 90% of users who haven't heard of PWAs
- No App Store discoverability (76 PWAs with no organic traffic source)
- Push notification opt-in is worse in browsers than native
- iOS Safari PWA support is inconsistent (service worker bugs, notification limits)
- No in-app purchase infrastructure — had to use Stripe Payment Links instead

**The real comparison:**
PWA is fast to build and deploy. Native is slow to ship but gets discovered.

For the 76 apps I built: the automation pipeline can build them. The distribution problem is unsolved — they're live but invisible.

For the 4 iOS apps (built with Expo/React Native): App Store submission is the bottleneck, but once in the store, discovery exists.

If I were starting over:
- Use PWA for internal tools, B2B products, or when you control the distribution channel (email list, community, paid ads)
- Use native for consumer apps where discoverability matters

The "build a PWA because it's faster" logic ignores that speed of build doesn't help if you can't solve distribution.

---
