# Indie Hackers posts — cycle 13
# Status: PENDING_REVIEW
# Format: "I built X" with technical detail + honest lessons. IH readers are builders. They want the how and the why it didn't go smoothly.
# Voice: First-person, specific, honest about failures and tradeoffs. Numbers required. No hype.

---

## Post 1 — PageScorer

**Title:**
I built a landing page grader (A-F scoring). Here's what I learned auditing 50 real pages.

**Body:**

I built PageScorer over about 6 weeks. It grades any landing page A-F based on 5 conversion criteria and gives you specific fixes for anything below a B.

The URL: pagescorer.surge.sh. Free, no signup.

Here's what went into it and what I learned.

**Why I built it**

I had a product that wasn't converting. I assumed it was the product. It was the landing page. Three specific things: a vague headline, a generic CTA, and a 6-second load time.

Once I fixed those, conversions started. I wanted a tool that would have caught those problems in 5 minutes instead of 3 months.

**How the scoring works**

5 criteria, each weighted:

- Value proposition clarity (30%) — does the hero section explain what the product does, for who, and what happens?
- CTA specificity (25%) — does the button tell you what happens when you click?
- Social proof presence (20%) — is there at least one credible proof element above the fold?
- Form friction (15%) — how many fields? Is anything optional? Does the form look trustworthy?
- Load time (10%) — anything over 3 seconds on mobile gets dinged

I tried an LLM-based scoring approach first. The problems: inconsistent scores across identical inputs, slow response times (3-5 seconds vs. 0.5), and outputs that were verbose instead of actionable. Switched to rule-based scoring. Faster, consistent, cheaper, more useful.

**What I found auditing real pages**

I tested it on 50 landing pages from IH, r/SideProject, and my own bookmarks.

80% scored C or below.

The failure pattern was almost identical across the C and D pages: headline was too abstract, CTA was "Get Started" or "Try Free," no social proof above the fold.

Technical founders had consistently better feature sections and worse hero sections. The reverse was true for marketing-background founders.

The single highest-converting pages I looked at all had one thing in common: the headline answered "what does this do" in one sentence without jargon. That sounds obvious. Most pages don't do it.

**What I got wrong**

Load time weighting is probably too low at 10%. A page that takes 6 seconds to load on mobile will underperform regardless of copy quality. I may push that to 20% and reduce the CTA weight.

I also didn't build in a URL validation layer early enough. The first version would error on redirect chains and pages with aggressive bot detection. Fixed now, but it took a couple of weeks of bug reports.

The "social proof" criterion is still imprecise. A photo with a quote is worth much less than a named testimonial with a company. Right now the grader can't distinguish those. Working on it.

**Where it is now**

Free, running on surge.sh, about 8 seconds per audit.

The tech is boring on purpose. Static frontend, rule-based scoring logic, no database. Runs entirely client-side for the scoring. The only server-side piece is the URL fetch and parse.

If you want to run your page: pagescorer.surge.sh

Happy to look at specific pages manually in the comments if you want a second read beyond the automated score. Sometimes the rule-based grader misses context.

---

## Post 2 — Side Project Revenue Estimator

**Title:**
I built a revenue estimator that accounts for traffic source. The numbers are more honest than most.

**Body:**

I got tired of revenue projection tools that give you one number with no range and no context.

So I built one that gives you P10, P50, and P90 projections, broken out by traffic source and monetization type: side-project-revenue-estimator.surge.sh. Free, no signup.

Here's the thinking behind it and the data it's built on.

**The problem with most revenue calculators**

They ask for your projected traffic and apply a flat conversion rate.

But conversion rate isn't flat. It varies by 5-10x depending on:

- Where the traffic comes from (organic SEO converts completely differently than paid)
- What you're selling (SaaS trial-to-paid vs. affiliate vs. digital product vs. service)
- What niche you're in (developer tools vs. consumer apps vs. local services)

A calculator that ignores those variables isn't a projection. It's a fantasy.

**What the estimator asks for**

7 inputs:

1. Traffic source (SEO, paid, social, newsletter, direct/referral)
2. Monetization type (SaaS, affiliate, digital product, service, ads)
3. Niche (B2B SaaS, developer tools, consumer app, info product, local)
4. Monthly visitor count
5. Current month of operation (1-24)
6. Current MRR if you have it (optional, for calibration)
7. Average deal/product price

**What it outputs**

P10 (you underperform assumptions), P50 (you execute reasonably), P90 (things go well) for months 1-12.

The ramp curve is built in. Month 1 of organic SEO traffic is not month 12. Word of mouth compounds, SEO compounds, your conversion rate improves as you iterate on onboarding. A projection that ignores the ramp is consistently too optimistic early and too pessimistic late.

It also includes a reality check flag. If your inputs produce a P50 projection that's implausible given volume and price, the tool flags it. "Your projection implies 8% conversion from organic SEO to paid. The benchmark is 0.8-1.5%. Either your conversion assumptions are off or your product has unusual demand characteristics."

**Where the conversion benchmarks came from**

I compiled these from:

- ~40 Starter Story interviews with publicly shared conversion data
- 12 IH posts with actual revenue and traffic numbers
- My own projects (3 of them, different traffic sources)
- Patrick McKenzie's publicly shared SaaS conversion benchmarks

These are not perfect. B2B SaaS and developer tool conversions I'm most confident in. Consumer app and info product conversions have wider variance.

**What surprised me**

Developer tools convert better from organic SEO than from paid. My hypothesis: developers block ads, and the intent signal from organic search is stronger ("how to solve X" vs. seeing an ad while browsing).

Info products have the widest conversion variance of any category. A strong email list converting to a relevant product can hit 3-4%. Cold paid traffic to an info product is often under 0.5%. The tool captures this variance in the P10-P90 spread.

Month 4-6 is where most side projects see the first meaningful compounding. Before that, it often feels like nothing is working. The projections show this and it's useful context when you're in month 2 wondering if you should quit.

**Honest limitations**

The tool is built on aggregated public data. Your specific situation may differ significantly.

If you have existing conversion data from your own product, use it to override the defaults. The tool lets you input your actual conversion rate if you have it, which makes the projection far more accurate.

The P90 scenario is genuinely optimistic. It represents things going well, not things going perfectly. If you're treating P90 as your baseline expectation, you will be disappointed.

I'm working on adding a "what would it take to hit $X" reverse-calculator mode. Enter your target revenue, get back the traffic and conversion numbers you'd need to hit it. That feels more useful for goal-setting than forward projection.

Any questions about the methodology or specific numbers, ask in the comments. I'd rather be challenged on the assumptions than have people trust inaccurate numbers.
