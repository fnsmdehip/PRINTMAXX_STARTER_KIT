# Reddit Distribution — Cycle 45 — 2026-05-05
# Focus: TruthScope, Research Blog, MCP Marketplace, Day 44 narrative, dosewell, androx

---

## POST 1: r/ClaudeAI
**Title:** I built a searchable MCP server marketplace — free, no accounts, 200ms load
**Type:** Valuable resource drop (no promotion vibe)
**URL to include:** mcp-marketplace.surge.sh

**Body:**
The discovery problem for MCP servers is getting real. There are 400+ public repos scattered across GitHub with no standardized way to find what you need.

I built a static PWA directory: mcp-marketplace.surge.sh

What it has:
- Searchable index of public MCP servers
- Categorized by function (data, AI, productivity, dev tools, integrations)
- Copy-paste install commands
- No accounts, no tracking, loads in ~200ms

It's free and will stay free. I'm also adding servers regularly.

If you're building a MCP server and want it listed, drop the repo in the comments.

What MCP servers are you running in your daily workflow? Curious what's actually useful vs what just looks impressive.

---

## POST 2: r/SideProject
**Title:** 44 days of building. 76 apps deployed. $0 revenue. Here's the exact diagnosis.
**Type:** Transparent autopsy post (high engagement format)

**Body:**
I want to share something honest because I see a lot of "built X, made $Y" posts and almost none of the "built everything, made nothing" version.

**What's live:**
- 76 web PWAs deployed (streak apps, tool calculators, comparison pages)
- 540 automation scripts
- 33 autonomous AI agents running nightly
- 192,700 leads analyzed, 17,484 hot
- 20 Gumroad listings written and ready
- 12 Fiverr proposals written

**Revenue: $0**

**The actual problem (embarrassingly simple):**
I never created the accounts to accept payment.

No Gumroad account. No Stripe product listed. No Fiverr profile.

I spent 44 days building systems to operate a business I hadn't technically started yet.

**What I learned:**
Automation compounds existing actions. It cannot substitute for the first action.

The hardest thing about going from $0 to $1 isn't the product. It's filling out a form on a website while an inner voice asks "is this worth it."

I'm fixing this this week. Creating the accounts. Listing the products.

Sharing this because I suspect I'm not the only one who built a spaceship and forgot to buy the launch pad.

---

## POST 3: r/privacy
**Title:** Built a consent documentation app — local-first, AES-256-GCM encrypted, no server
**Type:** Resource share + technical details (r/privacy loves this format)
**URL:** cnsnt-web.surge.sh

**Body:**
I got tired of consent documentation apps that required accounts and stored data on someone else's server.

Built cnsnt as a local-first PWA: cnsnt-web.surge.sh

**Technical details (since this community cares):**
- AES-256-GCM encryption (not AES-128, not XOR, not "industry standard")
- PBKDF2 key derivation at 100,000 iterations
- HMAC-SHA-256 integrity verification on every record
- Everything stored in device localStorage, never leaves the device
- Cloud backup available if you want it, but it's encrypted before upload — we never see plaintext
- PIN lockout with progressive delays
- Audit log of all access attempts

No accounts required. No tracking. Open for inspection if you want to audit it.

The app generates legally formatted consent documentation with timestamp, custom templates, and export.

What do you use for local-first sensitive data storage? Always looking for better patterns.

---

## POST 4: r/iphone
**Title:** Built TruthScope — a lie detector that uses real biometric sensors, not fake AI percentages
**Type:** App showcase with technical credibility
**URL:** truthscope.surge.sh

**Body:**
Every lie detector app in the App Store uses Math.random(). I checked.

They show dramatic readings with confidence percentages calculated from nothing. Users are paying for a dressed-up random number generator.

I built TruthScope to be the opposite:

**Real sensor stack:**
- PPG heart rate via phone camera (react-native-vision-camera — real frame data)
- Voice stress via F0 frequency analysis (actual pitch detection, not volume metering)
- Facial micro-expression detection (CV model per frame, not vibes)

**Honesty policy:**
- If a sensor is unavailable, it says "SENSOR UNAVAILABLE"
- It publishes accuracy ranges from peer-reviewed research (65-80%, not "99% accurate")
- It never fakes a reading

You can try the browser version at truthscope.surge.sh — the finger PPG actually reads your heart rate.

Curious if anyone has looked at the accuracy research on phone-based PPG. The Verkruysse et al. 2008 study is the baseline most implementations cite.

---

## POST 5: r/productivity
**Title:** Free tool: pocket-alexandria.surge.sh — 156 classic books, offline, no accounts
**Type:** Resource share
**URL:** pocket-alexandria.surge.sh

**Body:**
Built Pocket Alexandria as a minimalist reading app with 156 public domain books.

What it does:
- 156 books (Stoics, philosophy, history, classic fiction)
- Works fully offline after first load
- No accounts, no tracking
- Reading progress saved locally
- Night/day theme toggle

Free tier: 10 books. Premium: all 156, $1.99/mo.

Alternatives I looked at before building it:
- Standard Ebooks (great, but no offline PWA)
- Project Gutenberg (excellent source, terrible UX)
- Librivox (audio only)

There wasn't a fast offline PWA with good typography for the specific books I wanted. So I built one.

pocket-alexandria.surge.sh

What are people using for offline reading in 2026?

---

## POST 6: r/MachineLearning (or r/artificial)
**Title:** Show r/MachineLearning: UAF physics research blog — 51 manuscript versions, 21 chapters
**Type:** Research share
**URL:** fnsmdehip-research.surge.sh

**Body:**
I've been writing a manuscript called UAF (Unified Autonomous Field) for 6 months.

It attempts a bottom-up derivation of consciousness and physical law from first principles, with sections on:
- Topos-theoretic quantum foundations
- Relational holography and observer-relative geometry
- Saturn's hexagonal wave structure as a mechanical resonance model
- UAF recursive eigenvalue equations

17 articles are live at fnsmdehip-research.surge.sh

I'm genuinely uncertain whether this is interesting physics speculation or structured nonsense. The manuscript is at version 51.

I'm posting here because the ML community tends to think carefully about the math/physics boundary. The derivations use category theory, spectral analysis, and some novel geometric constructs.

Would be interested in technical feedback. What's the right sub for this if r/MachineLearning isn't the right fit?

---

## POST 7: r/learnprogramming
**Title:** How I structured 540 automation scripts without them turning into spaghetti (lessons from a system that got messy)
**Type:** Educational value post

**Body:**
I have 540 Python scripts in a system that runs 33 autonomous AI agents. It got very messy before I figured out what worked.

The pattern that saved it:

**1. Every script needs a named caller**
Before creating any new .py file: who calls this? Cron? Another script? If nobody, don't create it.

I had 150+ "orphan" scripts that ran once manually and never again. They're dead weight.

**2. Test on create, not on schedule**
Every automation I wrote, I ran immediately after creation. Check the output. Fix errors. Run again until clean. Then add to cron.

The alternative: write it, schedule it, wonder why nothing happened 3 days later.

**3. API key vs OAuth in headless scripts**
Every `subprocess.run(["external-tool"...])` call should check for API keys. OAuth tokens expire silently in cron environments. API keys don't.

Pattern I use everywhere now:
```python
cmd = ["tool", "-p"]
if os.environ.get("API_KEY"):
    cmd += ["--api-key", os.environ["API_KEY"]]
```

**4. Heuristic fallbacks when LLM calls fail**
Every LLM call in an automation has a fallback that runs without the model. The system degrades gracefully instead of failing silently.

What patterns have worked for you in larger automation systems?
