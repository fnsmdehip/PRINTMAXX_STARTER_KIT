# cnsnt Viral Campaign Brief - March 27, 2026

## Trigger Event
YouTuber Turkey Tom (1.6M subscribers) had abuse allegations retracted by his accuser in early March 2026. The accuser posted a public statement on Kiwi Farms admitting the claims were false and apologizing. This followed Tom's 40-minute defense video in February. The story trended across YouTube, Twitter/X, Reddit, and commentary channels (DramaAlert covered it).

**Pattern:** Allegation viral in hours. Defense takes months. Even after retraction, career damage is permanent. This pattern repeats weekly in the creator economy.

## Campaign Strategy
Ride the trending discourse around false accusations and creator vulnerability WITHOUT naming Turkey Tom directly. Position cnsnt as the solution to a systemic problem.

## Content Created

### Twitter/X Posts (10 total)
**File:** `CONTENT/social/posting_queue/cnsnt_viral_campaign_20260327.csv`

| Type | Count | Angle |
|------|-------|-------|
| Hot takes | 3 | "This is why you need receipts" / career russian roulette / pattern recognition |
| Educational | 3 | What a consent record looks like / speed of defense / trust is not a strategy |
| Engagement bait | 2 | "If you don't document consent in 2026..." / prenup normalization |
| Product mentions | 2 | Direct feature pitch / why texts aren't evidence |

**Posting schedule:** Stagger across 3 days. Hot takes first (ride the wave), educational next (build authority), product mentions last (convert).

### Reddit Posts (5 total)
**File:** `CONTENT/social/posting_queue/cnsnt_reddit_campaign_20260327.csv`

| Subreddit | Angle |
|-----------|-------|
| r/legaladvice | Legal evidence angle, lawyer feedback requested |
| r/privacy | Zero-data-collection architecture, privacy community feedback |
| r/selfimprovement | Seatbelt analogy, uncomfortable self-improvement |
| r/Entrepreneur | Market gap, creator economy liability, startup metrics |
| r/startups | Market sizing, untapped vertical thesis, GTM feedback |

**Posting schedule:** One per day across 5 days. Monday-Friday. Never post multiple on same day (spam detection).

### Landing Page
**File:** `LANDING/cnsnt/index.html`
**Deploy target:** `cnsnt-app.surge.sh`

Sections:
1. Nav with logo + Launch App CTA
2. Hero: urgency badge + headline + subtext + dual CTA (web app + iOS coming soon)
3. Social proof stats: AES-256 / 0 server data / 11 templates / 30s to create
4. Context card: the problem is getting worse (48hr sponsor drops, 18mo legal)
5. 6 feature cards: Encrypted, Local-First, Free, Timestamped, Templates, Audit Trail
6. How It Works: 4 steps
7. Pricing: Free ($0 forever) + Pro ($4.99/mo or $29.99/yr)
8. Privacy badge: "Your data never leaves your device"
9. FAQ: 7 questions covering legal admissibility, access, device loss, timestamps, use cases, data selling, trust model
10. Final CTA
11. Footer with privacy/terms/contact links

## Funnel Flow
```
Twitter post → cnsnt.surge.sh (web app) OR cnsnt-app.surge.sh (landing page)
Reddit post → cnsnt.surge.sh (web app)
Landing page → cnsnt.surge.sh (web app) + iOS App Store (when live)
```

## Key Messaging Framework
- **Never name specific people** (defamation risk)
- **Frame as systemic problem** not individual drama
- **Both parties benefit** from documentation (not adversarial)
- **Speed argument:** internet is faster than courts, documentation closes the gap
- **Seatbelt analogy:** hope you never need it, but if you do, it changes everything
- **Trust is not a strategy:** contracts exist because trust isn't enough

## Metrics to Track
- Landing page visits (surge analytics or add simple counter)
- Web app opens from campaign links
- Twitter engagement (likes, retweets, replies, quote tweets)
- Reddit upvotes and comment sentiment
- App Store installs (when iOS version is live)

## Human Actions Required
1. **Post the tweets** from personal Twitter/X account (stagger over 3 days)
2. **Post Reddit threads** from established Reddit account (1 per day, 5 days)
3. **Deploy landing page** if surge CLI deployment needs auth
4. **Monitor replies** and engage with comments (builds authority)

## Risk Mitigation
- No specific names mentioned anywhere = zero defamation risk
- All claims about cnsnt are accurate (AES-256, local-first, free)
- Reddit posts framed as "I built this" = genuine, not astroturfed
- Landing page has no fake metrics or false social proof
