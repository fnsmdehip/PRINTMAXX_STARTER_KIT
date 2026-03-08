# Local Biz Cold Email Follow-Up Sequence

**Purpose:** Follow up on cold audit emails that got no reply
**Emails:** 3
**Timing:** Days 3, 7, 14 after initial email
**Goal:** Get "interested" reply for video walkthrough
**Pairs with:** AUTOMATIONS/leads/COLD_EMAILS_READY_TO_SEND.md

---

## How to Use This Sequence

Each follow-up has a **generic template** and **per-category variants** (dental, restaurant, lawyer). Pick the variant that matches the lead.

For each follow-up, replace:
- `[DOMAIN]` with the business website
- `[ISSUE]` with their #1 problem from the initial email
- `[SPECIFIC_DETAIL]` from the initial audit

---

## Follow-Up 1: The Proof Drop (Day 3)

**Subject:** re: [original subject line]

**Why it works:** Reply to the original thread. No new subject line. Gmail/Outlook shows it as a continuation, not a new cold email. Open rates 2-3x higher on replies.

### Template (Generic)

hey,

sent you a note about [DOMAIN] a few days ago.

quick update: I ran [DOMAIN] through google's pagespeed insights. here's what it said:

- performance score: [XX]/100
- [ISSUE]: google flags this as a problem
- estimated traffic loss: [XX]% of mobile visitors bounce immediately

not trying to sell you anything. just figured you'd want to know what google actually thinks of your site.

reply "interested" if you want the 3-minute video walkthrough. takes me 10 minutes to make, costs you nothing.

### Dental Variant

hey,

sent you a note about [DOMAIN] a few days ago.

quick thing: I checked how [DOMAIN] shows up when someone googles "[CITY] dentist" on their phone. the result loads, but the site doesn't resize. buttons overlap. text is unreadable.

patients see that and hit back. they don't call. they don't book. they just leave.

your competitors with mobile-friendly sites are catching those patients right now.

reply "interested" and I'll record a 3-minute video showing exactly what patients see on their phones vs what your competitors show.

### Restaurant Variant

hey,

sent you a note about [DOMAIN] a few days ago.

one thing I didn't mention: when someone googles "[RESTAURANT_NAME] [CITY]," your competitors with schema markup show hours, ratings, price range, and photos directly in google results. your listing shows up as plain text.

that's the difference between someone clicking your result and clicking the restaurant below you.

reply "interested" and I'll show you exactly what this looks like in a 3-minute video.

### Lawyer Variant

hey,

sent you a note about [DOMAIN] a few days ago.

ran one more check: searched "[PRACTICE_AREA] lawyer [CITY]" on google. your listing appears, but without schema markup it shows as plain text. no ratings, no practice areas, no phone number in the snippet.

attorneys with schema show all of that directly in the search result. clients click them first because they look more established.

reply "interested" and I'll send a 3-minute comparison video of your listing vs the top 3 results.

---

## Follow-Up 2: The Competitor Move (Day 7)

**Subject:** re: [original subject line]

**Why it works:** Competitor intelligence triggers loss aversion. People don't act on their own problems. They act when competitors are beating them.

### Template (Generic)

hey,

last email on this.

I looked at your top 3 competitors in [CITY]:

- [COMPETITOR_1]: mobile friendly, schema markup, loads in 1.2s
- [COMPETITOR_2]: SSL, contact form, social links
- [DOMAIN]: [TOP_ISSUE_1], [TOP_ISSUE_2], [TOP_ISSUE_3]

not saying they're better at what you do. but google doesn't know that. google ranks based on site quality, not service quality.

the fixes for [DOMAIN] are all under $500 and take less than a week. most are under $200.

reply "interested" and I'll break down the exact fixes in order of impact.

or reply "remove" and I'll stop emailing.

### Dental Variant

hey,

last follow-up on this.

checked 3 dental practices near you in [CITY]:

- [COMPETITOR_1]: mobile site, online booking, SSL, loads in 1.4s
- [COMPETITOR_2]: schema markup (hours and ratings show in google), contact form
- [DOMAIN]: [TOP_ISSUE_1], [TOP_ISSUE_2], [TOP_ISSUE_3]

a new patient googles "[CITY] dentist." they see all 3 results. they click the one that looks most professional and has online booking.

the gap between your site and theirs is fixable. most of it in a weekend.

reply "interested" for the video walkthrough, or "remove" to stop hearing from me.

### Restaurant Variant

hey,

final note on [DOMAIN].

compared your google presence to 2 nearby restaurants:

- [COMPETITOR_1]: hours, photos, price range, ratings all showing in google results
- [COMPETITOR_2]: mobile friendly, 1.1s load time, reservation link in the listing
- [DOMAIN]: [TOP_ISSUE_1], [TOP_ISSUE_2], [TOP_ISSUE_3]

when someone searches "dinner in [CITY]," the restaurants with schema and fast sites win the click. every time.

your food might be better. google doesn't know that.

reply "interested" and I'll show you the comparison in a 3-minute video. or "remove" and I'll stop.

### Lawyer Variant

hey,

last email about [DOMAIN].

compared your site to 2 firms ranking above you for "[PRACTICE_AREA] [CITY]":

- [COMPETITOR_1]: schema markup (practice areas, ratings in google snippet), mobile friendly
- [COMPETITOR_2]: SSL, contact form, 0.9s load time, structured data
- [DOMAIN]: [TOP_ISSUE_1], [TOP_ISSUE_2], [TOP_ISSUE_3]

potential clients compare these 3 results side by side. the firm that looks most established online gets the call.

reply "interested" for the breakdown, or "remove" and I'll delete your info.

---

## Follow-Up 3: The Breakup Email (Day 14)

**Subject:** should I close your file?

**Why it works:** New subject line. Breakup emails get 30-40% open rates because they trigger fear of missing out. "close your file" implies there's a file worth keeping open.

### Template (All Categories)

hey,

I've sent a few emails about [DOMAIN]. no response, so I'll assume the timing isn't right.

I'm closing your file. if you ever want the free site audit video, just reply to any of my emails and I'll make it.

one last thing: the [TOP_ISSUE] on [DOMAIN] gets worse over time, not better. google re-crawls sites and adjusts rankings. sites that don't improve gradually lose position to sites that do.

no hard feelings either way.

reply "interested" if you change your mind. reply "remove" to never hear from me again.

---

## Sequence Automation Notes

### Timing Logic
- Day 0: Send initial email (from COLD_EMAILS_READY_TO_SEND.md)
- Day 3: Follow-Up 1 (proof drop) — reply to original thread
- Day 7: Follow-Up 2 (competitor move) — reply to original thread
- Day 14: Follow-Up 3 (breakup) — new subject line "should I close your file?"

### Reply Detection
- If they reply "interested" at ANY point: stop sequence, record loom video, send pricing
- If they reply "remove" at ANY point: stop sequence, mark as unsubscribed, never email again
- If they reply with a question: stop sequence, answer question, then offer video

### Loom Video Template (When They Reply "Interested")
1. Open their site in browser (0:00-0:10)
2. Show google mobile-friendly test results (0:10-0:30)
3. Show google pagespeed insights (0:30-1:00)
4. Show competitor comparison (1:00-1:30)
5. Walk through top 3 fixes in order of impact (1:30-2:30)
6. End with: "these fixes take [X] hours. I charge [$X] for the full package. reply if you want details." (2:30-3:00)

### Pricing (Include at End of Loom Video)
- Basic audit report (PDF): free (already done)
- SSL + mobile fix: $200-400
- Full site optimization (SSL + mobile + schema + speed + SEO basics): $500-800
- Monthly maintenance (updates + monitoring + monthly report): $100/month
- Bundle: full optimization + 3 months maintenance: $800

### CAN-SPAM Compliance
- Every email includes "reply remove to unsubscribe"
- Physical address required (add to email signature)
- Honor remove requests within 24 hours
- Track all sent emails in LEDGER/OUTREACH_TRACKER.csv

### Metrics to Track
- Initial email open rate (target: 40-60%)
- Follow-up 1 open rate (target: 50-70% — reply thread boost)
- Follow-up 2 open rate (target: 30-50%)
- Follow-up 3 open rate (target: 30-40% — breakup boost)
- Overall reply rate (target: 5-15%)
- "Interested" rate (target: 3-8%)
- Video-to-close rate (target: 20-40%)

### Per-Lead Customization Guide

| Lead | Follow-Up 1 Proof | Follow-Up 2 Competitors | Breakup Top Issue |
|------|-------------------|------------------------|-------------------|
| Houston Dentists | chrome "not secure" warning screenshot | healthyteethhouston.com, dentalgeekshouston.com | no SSL |
| Metro Dental Atlanta | google mobile-friendly test fail | nearby atlanta dental practices | not mobile friendly |
| The Doctor's Office | no meta description = google guessing | seattle restaurants with schema | not mobile friendly |
| Atlanta Bar Assoc | jQuery 2 CVE list | state bar associations with modern stacks | jQuery 2 security |
| Villalobos Law | 0.8s speed vs mobile fail contrast | chicago firms with mobile + forms | not mobile friendly |
| Dallas Bar Assoc | search snippet comparison (theirs vs optimized) | atlanta bar, other state bars | no meta description |
| Canlis | competitor schema in google results | seattle fine dining with rich snippets | no schema |
| Ultreia Denver | pagespeed insights 3.2s screenshot | denver restaurants under 2s load time | slow load time |
| Rioja Denver | pagespeed insights 3.8s screenshot | denver restaurants under 2s load time | slow load time |
| Seattle Restaurant Alliance | search snippet with vs without schema | similar wordpress organizations | no schema |

---

*Last updated: 2026-03-08*
*80% of deals close after the 5th touchpoint. most people stop at 1.*

---

*Disclaimer: Results not typical. Individual results vary based on effort, market conditions, and other factors.*
