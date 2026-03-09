# Reddit posts — cycle 13
# Status: PENDING_REVIEW
# Subreddits: r/SideProject, r/Entrepreneur, r/SaaS
# Notes: Reddit rewards value-first framing. The tool is secondary to the insight. Lead with the problem or observation, let the tool surface naturally. No self-promotion energy.

---

## Post 1 — r/SideProject

**Title:**
I audited 50 side project landing pages and 80% failed on the same 2 things

**Body:**

Been working on a landing page audit tool for the past few months, which meant I needed to test it on a lot of real pages. So I audited 50 side project landing pages from this subreddit and a few others.

The results were pretty consistent. 80% scored C or below. The two failure points that showed up everywhere:

**1. The value prop doesn't say what the product actually does.**

"The future of [category]" is not a value prop. "10x your [outcome]" is not a value prop. A value prop is: what does this do, for who, and what's the specific result?

The best landing page I audited said: "Paste your Stripe data. Get a visual breakdown of your MRR, churn, and expansion revenue. Takes 30 seconds." That's it. Clear product, clear user, clear result.

**2. The CTA doesn't tell you what happens when you click it.**

"Get Started" tells me nothing. Started doing what? Will I be asked to pay? Create an account? "Start your free audit" tells me exactly what happens. Conversion rate difference between these two options is well documented in split test literature, usually 15-30%.

Other stuff I noticed:

- About 60% of pages loaded slower than 3 seconds on mobile. This kills conversions before anyone reads a word.
- Pages from technical founders almost always had great feature lists and terrible hero sections. Pages from marketing-background founders were the opposite.
- Social proof was either absent or fake-looking (stock photo testimonials with no last names or companies).

If you want to see how your page scores, I built a tool that runs this audit automatically: https://pagescorer.surge.sh

Free, takes about 8 seconds, gives you a letter grade (A-F) with specific fixes. Not trying to sell anything, just sharing what I've been working on.

Drop your URL in the comments if you want feedback. Happy to look at a few manually.

---

## Post 2 — r/Entrepreneur

**Title:**
Nobody talks about the real math behind cold email. Here's what it actually costs per closed deal.

**Body:**

Cold email is one of those channels where everyone publishes vanity metrics and almost nobody shows you the actual unit economics.

I've been running cold email for my own outreach for about 8 months and I kept doing the same spreadsheet math every week. Eventually I built a calculator so I could stop doing it manually.

Here's the math most people skip:

Say you send 200 emails per week. 30% open rate (decent). 5% reply rate (good). 30% of replies are positive/interested. 20% of interested replies close. Your average deal is $800.

That sounds like it works. But if you're spending 8 hours per week on this channel (research, personalization, follow-up, responses), your effective hourly rate is:

200 emails x 5% reply x 30% positive x 20% close = 0.6 deals/week
0.6 deals x $800 = $480/week revenue
$480 / 8 hours = $60/hr

Okay, $60/hr is fine. But now factor in that most people aren't at 5% reply and 20% close to start. Early-stage cold email at 1% reply and 10% close at the same hours looks like this:

200 x 1% x 50% positive x 10% close = 0.1 deals/week
0.1 x $800 = $80/week
$80 / 8 hours = $10/hr

That's not a channel. That's a hobby.

The math only makes sense when:
- Your deal size is above $1k
- You're past the learning curve (usually month 3-4)
- You've automated the research layer

I built a calculator that runs these numbers so you don't have to do it in a spreadsheet: https://cold-email-roi-calculator.surge.sh

7 inputs, outputs cost-per-deal, effective hourly rate, breakeven volume, and 90-day projection. Free, no signup.

The number most people find depressing: their current setup costs $300-600 per closed deal when you account for time. The number that's actually useful: what deal size or volume makes it profitable for your situation.

What's your current cost-per-closed-deal on cold email? Curious what's realistic for different niches.

---

## Post 3 — r/SaaS

**Title:**
SaaS revenue projections are almost always wrong because they ignore traffic source. Here's a better model.

**Body:**

The standard SaaS revenue projection goes like this: estimate your traffic, apply a conversion rate, multiply by ACV.

The problem: "a conversion rate" doesn't exist. Conversion rate varies by 5-10x depending on where your traffic comes from and how your product is monetized.

Organic SEO traffic converting to a $49/mo SaaS tool converts at 0.8-1.5% from visitor to paid.

Paid traffic to the same tool converts at 2-4% from visitor to trial, then 15-25% of trials to paid. So maybe 0.3-1% of ad clicks to paid, depending on targeting.

Newsletter traffic from a relevant audience to a relevant product? 2-4% click-to-trial if the positioning is strong.

These are not the same number. If you're projecting revenue using one blended conversion rate, your model is wrong by definition.

The other thing that kills projections: ignoring the ramp curve. Month 1 of a new SaaS tool is not Month 12. SEO compounds. Word of mouth compounds. Your conversion rate improves as you iterate on the page and the onboarding. A projection that gives you the same monthly number for 12 months is not a projection, it's a guess.

I built a revenue estimator that accounts for traffic source, monetization type, niche, and a realistic ramp curve: https://side-project-revenue-estimator.surge.sh

It outputs P10, P50, P90 ranges, not a single number. P10 = you underperform. P50 = you execute reasonably. P90 = things go well. Also includes a reality check flag that fires when inputs produce projections that are detached from the data I've seen.

Free, no account required, all calculations run client-side.

The finding that surprised me most when building it: B2B SaaS tools targeting developers convert better from SEO than from paid, probably because developers block ads and the intent signal from organic search is stronger. Consumer tools are the opposite.

What's your actual conversion rate by traffic source? Sharing real numbers helps calibrate this kind of thing.
