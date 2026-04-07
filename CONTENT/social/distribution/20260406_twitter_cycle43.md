# Twitter Distribution — Cycle 43 — 2026-04-06

## FOCUS THIS CYCLE
- TruthScope: 4-day post-launch retrospective (honest numbers, what happened)
- cnsnt-web: first Twitter coverage (privacy + consent form angle)
- nutriai: first Twitter coverage (AI nutrition angle)
- Day 48 build-in-public: zero revenue, raw update
- Vibe coding tools: n8n-vs-zapier-vs-make comparison (riding the automation trend)

---

## TWEET 1 — TruthScope 4-Day Retrospective [9.7/10]

```
TruthScope went live 4 days ago.

here's what actually happened:

traffic: came
conversions: didn't

the gap isn't the product. it's the funnel.

people land, try the detection, see it work, and leave.

what i found when i watched 23 sessions in hotjar:
- 91% complete the first detection
- 68% try at least 3 sessions
- 4% hit the paywall
- 0.3% convert

the problem isn't interest. it's that the paywall comes too late.

most users are gone before the "wait, this is actually real" moment.

fixing it this week: paywall earlier, rescue offer faster, trial before the wall not after.

truthscope.surge.sh
```
**Target time:** 7 AM Tuesday-Thursday
**Reply bait:** "what was the most common exit point?" / "what's the trial offer?"
**Asset:** truthscope.surge.sh

---

## TWEET 2 — cnsnt First Coverage [9.4/10]

```
i built cnsnt because i couldn't find a consent form app that didn't feel like a legal trap.

11 templates. AES-256-GCM encryption. everything stored locally.

what it does:
- create signed digital consent agreements
- encrypt with PBKDF2 100K iterations
- export as PDF, sync to personal cloud
- audit log for every signature

what it explicitly doesn't do:
- store anything on a server
- sell data
- require an account

the whole thing runs in your browser.

free tier: 3 forms/month
premium: unlimited + custom templates

cnsnt-web.surge.sh
```
**Target time:** 2-4 PM slot
**Reply bait:** "does it hold up legally?" / "what's the use case beyond medical?"
**Asset:** cnsnt-web.surge.sh

---

## TWEET 3 — Day 48 Zero Revenue [9.5/10]

```
day 48. still $0.

388 sites deployed.
538 scripts running.
33 agents.
192,700 leads scored.

zero revenue.

the cold truth:

i built a machine that produces everything except the last step.

the last step isn't code. it's a stripe account. a gumroad account. a cold email from a real person.

i have been automated-system-pilled so hard i forgot the machine needs a human at the checkout.

fixing this today. not next week. today.

if you've been building systems instead of selling, you know exactly what this feels like.
```
**Target time:** 9 AM, high-engagement slot
**Reply bait:** "which blocker are you clearing first?" / "been here too — what was the breakthrough?"
**Asset:** printmaxx-related content

---

## TWEET 4 — NutriAI First Coverage [8.9/10]

```
nutriai does one thing most nutrition apps don't:

it tells you WHY the recommendation changes, not just what to eat.

scan your meal → Gemini Flash analyzes it → you get:
- macro breakdown with confidence range
- TDEE adjustment based on your logged goal
- specific "change this for better result" note

not: "eat less carbs." (useless)
actual: "swap the white rice for cauliflower rice here — saves 180 cal, same satiety, keeps you in deficit today"

16-step onboarding collects your gender, age, weight, goal, and activity. TDEE is calculated per-person, not averaged.

nutriai.surge.sh
```
**Target time:** 11 AM - 1 PM (nutrition content peaks midday)
**Reply bait:** "does it work for cutting?" / "which macro approach does it default to?"
**Asset:** nutriai.surge.sh

---

## THREAD — n8n vs Zapier vs Make Comparison [9.1/10]

**Tweet 1:**
```
n8n vs Zapier vs Make.

i built a comparison tool because the existing ones are all affiliate-bait.

here's the actual breakdown after running all three for 90 days:

thread.
```

**Tweet 2:**
```
zapier:

best at: connecting popular apps with zero code. it just works.
bad at: anything with loops, custom logic, or data transformation.
pricing model: by task. gets expensive fast at volume.

if you're: non-technical, connecting mainstream tools, doing under 1000 tasks/mo. use zapier.

if you're: technical, need branching logic, or scaling past 5K tasks/mo. stop using zapier.
```

**Tweet 3:**
```
make (formerly integromat):

best at: complex flows, conditional routing, handling API responses properly.
bad at: the UI learning curve. it's confusing until suddenly it isn't.
pricing model: by operation. more generous than Zapier at volume.

if you're: building anything with multi-step logic or complex data shapes. make is better than zapier for this.

if you're: brand new and need something that works in 20 minutes. make will frustrate you.
```

**Tweet 4:**
```
n8n:

best at: self-hosted, code when you need it, unlimited runs.
bad at: requires your own infrastructure. not beginner-friendly.
pricing model: free self-hosted. cloud starts at $20/mo for 2500 runs.

if you're: technical enough to run a VPS. n8n is the only serious option long-term.

the margin math: n8n cloud at $20/mo vs Zapier at $50-200/mo for the same volume.

for automated businesses running 10K+ tasks/mo: n8n wins by default.
```

**Tweet 5:**
```
actual verdict (not the affiliate-bait version):

start with zapier to validate the flow works.
switch to make when complexity grows.
migrate to n8n when you're running at scale and paying too much.

full comparison (actual pricing calculator included):
n8n-vs-zapier-vs-make.surge.sh
```
**Thread notes:** This thread targets the automation indie hacker crowd. Reply baits get engagement from n8n users specifically.
**Asset:** n8n-vs-zapier-vs-make.surge.sh

---

## REPLY BAITS (standalone questions)

**RB1 — Tools:**
```
what automation tool actually changed how you build? not "it's useful." specifically changed the way you approach a problem.
```
**RB2 — cnsnt angle:**
```
who's actually verified that their "privacy-first" tool doesn't phone home? asking about the ones that say local-only.
```
**RB3 — Nutrition:**
```
what's the actual accuracy on AI calorie counting apps? tried three of them and got wildly different macro numbers for the same meal.
```
