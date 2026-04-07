# Reddit Posts: Apps and Tools Distribution
# Date: 20260406
# Assets: TruthScope, cnsnt, comparison pages, cold email product

---

## POST 1
**Subreddit:** r/privacy
**Title:** I built a consent documentation app with AES-256-GCM encryption that stores nothing in the cloud. Here's the full crypto stack.

**Body:**

Built cnsnt because every consent app I found either stored data on company servers or used "encryption" that was basically base64 encoding.

For sensitive records, neither is acceptable.

Full cryptographic stack:

**Key derivation:** PBKDF2 with 100,000 iterations. Input is the user's PIN + a random salt stored locally. This produces the master key. 100K iterations means a brute-force attack on a 6-digit PIN takes hours, not milliseconds.

**Encryption:** AES-256-GCM. The GCM (Galois/Counter Mode) part is important. It provides authenticated encryption — any tampering with the ciphertext is detectable. Not just confidentiality, but integrity.

**Audit log:** HMAC-SHA-256 on each entry, with each entry including the hash of the previous entry. Makes the log append-only in a verifiable sense — you can't silently delete or edit a past entry without breaking the chain.

**Storage:** Device only. Optional iCloud backup is encrypted before it leaves the device.

**What this means practically:** If someone gets physical access to the device without the PIN, the records are protected. If our backend (we don't have one) were breached, there's nothing to exfiltrate.

Web version: cnsnt-web.surge.sh
iOS app: pending App Store review
macOS: cnsnt-downloads.surge.sh

Happy to discuss the crypto choices — particularly the PBKDF2 iteration count, which some people think should be higher (and they're not wrong).

---

## POST 2
**Subreddit:** r/iphone
**Title:** Built a stress detection app that actually uses real biometric sensors (not Math.random)

**Body:**

After seeing how many iOS "lie detector" and "stress detection" apps use fake data, I built TruthScope to show what real multi-signal detection looks like.

3 actual sensor inputs:

**PPG via rear camera:** You put your finger on the lens. The camera captures green channel pixel fluctuations caused by blood volume changes. Real photoplethysmography — the same principle as the sensor in your Apple Watch, just less precise on a phone camera. We process ~900 frames per 30-second session.

**Voice stress analysis:** Pitch extraction (F0), jitter, shimmer, harmonics-to-noise ratio from the microphone. These are the actual acoustic features researchers use to study vocal stress — not just "volume" or "frequency" as a proxy.

**Facial micro-expressions:** Action Unit detection from the front camera. Specific muscle group movements (AU4, AU6, AU7, AU17, AU23) that correlate with stress responses. Not face recognition — just feature tracking.

All 3 combine into a weighted fusion score.

Honest caveat: phone sensors are less precise than dedicated equipment. The app says this. "Medical grade" claims are marketing, not reality for consumer hardware.

Party Mode: 4 players place finger on camera sequentially, ranked by stress level. Genuinely fun at gatherings.

Web version: truthscope.surge.sh
iOS app: in development

---

## POST 3
**Subreddit:** r/productivity
**Title:** Comparing newsletter platforms for solopreneurs: what actually matters beyond price

**Body:**

I maintain a comparison page on newsletter platforms and wanted to share what I've found after building for this space.

The metrics people optimize for vs. what actually matters:

**Price (over-optimized):** Kit at $29/month vs. Beehiiv at $39/month is irrelevant if Beehiiv's native ad network monetizes 5x more. Price per subscriber matters less than revenue per subscriber.

**Open rates (slightly over-optimized):** Apple MPP inflated everyone's open rates. Real engagement metric is click rate. Platforms that show you click-to-open rate are more honest.

**Deliverability (under-optimized):** Most people never test this. Send to a Gmail + Outlook + Yahoo inbox from each platform before committing. Deliverability varies more than pricing pages suggest.

**Migration (severely under-optimized):** Switching platforms is painful. Subscriber lists move. RSS integrations break. Automations need rebuilding. The platform you start on is the platform you're probably on at 10K subscribers, so the 5-year total cost of ownership matters more than month 1 price.

**For most solopreneurs starting out:** Beehiiv's free tier (2,500 subscribers) and built-in ad network is the better starting point than Kit if you want to monetize via ads. Kit's automation is better if you're selling products to the list.

Full comparison at best-email-newsletter-platform.surge.sh if useful.

---

## POST 4
**Subreddit:** r/Entrepreneur
**Title:** n8n vs Zapier vs Make: the honest breakdown after using all three for automation

**Body:**

I built comparison pages for automation tools and want to share what I found after actually using all three for the same workflows.

**Where Zapier wins:**
- Onboarding (5 minutes to first working zap)
- App compatibility (7,000+ native integrations)
- Non-technical users who need it to just work
- Support quality when things break

**Where Make wins:**
- Visual workflow builder is genuinely easier to reason about complex flows
- Cost per task at scale (5-10x cheaper than Zapier for same workload)
- Custom HTTP request handling
- Error handling and branching logic

**Where n8n wins:**
- Self-hosted option ($0 for infrastructure)
- Code nodes (real JavaScript/Python)
- No per-task pricing (self-hosted = unlimited)
- Best for technical users who want control

**Honest take on switching costs:**
All three use different trigger/action paradigms. Workflows don't migrate. If you build 50 zaps and want to switch to Make, you're rebuilding from scratch.

Pick the one that fits your current volume and technical comfort, not the one that theoretically scales better. You can always migrate when you outgrow it.

Full comparison with pricing tables: n8n-vs-zapier-vs-make.surge.sh

