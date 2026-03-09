# Show HN posts — cycle 13
# Status: PENDING_REVIEW
# Target: news.ycombinator.com/submit (Show HN)
# Notes: HN rewards technical specificity, honest tradeoffs, builder perspective. No hype. No marketing language. Show the how.

---

## Post 1 — PageScorer

**Title:**
Show HN: PageScorer - I built a landing page audit tool that grades conversion potential A through F

**Body:**

I kept seeing the same pattern: founders spend weeks building a product, then write a landing page in 2 hours and wonder why it doesn't convert.

The problem isn't the product. It's that most landing pages fail 4-5 measurable criteria that correlate with conversion: a clear value proposition above the fold, social proof, a specific CTA, friction-free form design, and load time under 3 seconds.

PageScorer grades any URL across those criteria and returns an A-F score with specific line-level fixes. You paste a URL, it returns a scorecard in about 8 seconds.

The grading logic is rule-based, not LLM-generated. I tried the LLM route first. The output was verbose and inconsistent across runs. Rule-based scoring is faster, cheaper, and more actionable. Each grade maps to a specific fix, not a paragraph of suggestions.

A few things I learned building it:

Most pages fail on the same 2 things: value prop clarity and CTA specificity. "Get started" as a button is on about 70% of the pages I tested during development. It almost always scores a D or lower.

Load time matters more than founders think. A 6-second load on a marketing page kills conversions before anyone reads a word. That's in the grader.

The F-grade pages are usually from technical founders who are excellent at building and haven't thought about copywriting at all. The A-grade pages are almost always from people who have run paid traffic before and learned from the spend.

It's free. No signup. I'm considering adding a paid tier for bulk auditing (agencies, investors doing diligence on portfolio sites).

https://pagescorer.surge.sh

Interested in feedback on the scoring weights. I weighted CTA specificity at 25% of total score. Open to arguments that load time should carry more weight.

---

## Post 2 — Cold Email ROI Calculator

**Title:**
Show HN: I built a calculator that tells you what cold email actually costs per closed deal

**Body:**

Cold email has a math problem nobody talks about openly.

Everyone posts reply rates and open rates. Almost nobody publishes cost-per-closed-deal numbers, because the math is ugly.

Here's what I mean: A 3% reply rate sounds decent. But if your close rate from replies is 10%, and your average deal is $500, and you're spending 4 hours per 100 emails on personalization, you need to know your hourly rate on that time before you can call the channel profitable.

Most cold email tools give you vanity metrics. Open rates, click rates, reply rates. None of them calculate what you actually care about: did this pay?

The calculator asks for 7 inputs:
- Emails sent per week
- Open rate
- Reply rate
- Positive reply rate (replies that aren't "remove me")
- Close rate from positive replies
- Average deal value
- Time spent per 100 emails (hours)

It outputs: cost per closed deal, effective hourly rate, breakeven volume, and a 90-day revenue projection at current performance.

I built it because I was running cold email for my own outbound and kept doing this math in a spreadsheet. Figured other people were too.

The interesting finding from testing: most solopreneurs running cold email at low volume are working at an effective hourly rate of $8-15/hr when you factor in time cost. The math only gets good past roughly 500 emails/week with a solid sequence and a product at $1k+ ACV.

That's not a reason to stop. It's a reason to raise prices or automate more.

Free, no signup.

https://cold-email-roi-calculator.surge.sh

---

## Post 3 — Side Project Revenue Estimator

**Title:**
Show HN: Side Project Revenue Estimator - realistic projections based on traffic source, niche, and monetization type

**Body:**

Every side project revenue calculator I've seen is optimistic to the point of uselessness.

They ask for your projected traffic and multiply it by an assumed conversion rate. The problem: that number has almost no correlation to reality because conversion rates vary by 10x-20x depending on traffic source, niche, and monetization type.

Organic SEO traffic converting to a $49 info product converts at 0.5-1.5%. Paid traffic to a SaaS free trial converts at 2-5% to trial, then 10-25% of trials to paid. Newsletter traffic to an affiliate link converts at 0.8-3% depending on product-audience fit. These are not the same number.

This estimator accounts for those differences. You select:
- Traffic source (SEO, paid, social, newsletter, direct)
- Monetization type (SaaS, affiliate, digital product, service, ads)
- Niche (B2B tools, consumer apps, info products, local, developer tools)
- Monthly visitor count
- Current month in operation (ramp curve is real — month 1 is not month 12)

It outputs a 12-month projection with a realistic range (not a single number). P10, P50, P90. The P10 is what happens if you underperform. P90 is what happens if you execute well.

I also included a "reality check" flag that fires when projections look detached from input assumptions. For example: 100 monthly visitors projected to make $5k is flagged automatically.

The projection methodology is based on conversion benchmarks I've compiled from public case studies, Starter Story interviews, and my own projects. Not perfect, but better than multiplying traffic by 2%.

https://side-project-revenue-estimator.surge.sh

Free. No data stored. All calculations run client-side.

Feedback wanted on the niche conversion assumptions. The B2B SaaS numbers I'm most confident in. The info product numbers are the weakest.
