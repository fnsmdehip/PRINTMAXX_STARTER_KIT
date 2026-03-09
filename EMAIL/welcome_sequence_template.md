# Email Welcome Sequence — Ready for ConvertKit/Beehiiv
# Status: TEMPLATE READY (deploy when ESP account created)
# Trigger: New email signup from any lead magnet or comparison page
# Sequence: 5 emails over 7 days
# Copy style: PRINTMAXXER voice — lowercase, specific numbers, no AI slop

---

## EMAIL 1 — Immediate (0 min delay)
**Subject:** here's your [TOOL_NAME]
**Preview:** no tricks. just the tool.

hey —

you signed up for [TOOL_NAME]. here it is:

[TOOL_LINK]

bookmark it. it works offline too.

i build free tools for solopreneurs. no courses. no $997 masterminds. just tools that do one thing well.

here's what else i built (all free):
- cold email ROI calculator: https://cold-email-roi-calculator.surge.sh
- SaaS stack audit: https://saas-stack-audit.surge.sh
- revenue leak finder: https://revenue-leak-audit.surge.sh

reply to this email if any of them break. i fix things fast.

— printmaxx

---

## EMAIL 2 — Day 1 (24h delay)
**Subject:** the $127/mo mistake most solopreneurs make
**Preview:** i was making it too

quick one.

i ran a SaaS stack audit on my own setup last month. found $127/mo in overlapping tools.

notion + linear + todoist = 3 task managers. paying for all 3.
zapier + make = same automations on 2 platforms.
3 analytics tools tracking the same 4 metrics.

if you haven't audited your tool stack recently: https://saas-stack-audit.surge.sh

takes 2 minutes. most people find $50-150/mo they're wasting.

— printmaxx

---

## EMAIL 3 — Day 3 (72h delay)
**Subject:** your side project math (honest version)
**Preview:** most calculators lie. this one doesn't.

i built a revenue estimator for side projects.

it uses real benchmark data from 200+ indie projects. not "if you get 10,000 users" fantasy math.

the kind of math where:
- month 1 revenue is usually $0-50
- churn eats 5-8% per month for SaaS
- pricing under $10/mo almost never works at small scale

plug in your numbers: https://side-project-revenue-estimator.surge.sh

if the calculator says your idea is viable, build it. if it says no, save yourself 3 months.

— printmaxx

---

## EMAIL 4 — Day 5 (120h delay)
**Subject:** 11 tools. one person. $0 marketing budget.
**Preview:** everything i built this month

building in public update.

this month i shipped:
- 8 apps (all free, all work offline)
- 11 business tools (calculators, audits, checklists)
- 5 comparison pages (real benchmarks, not affiliate fluff)

total marketing budget: $0
total tool cost: $234/mo (claude max + hosting)

everything is at: https://app-hub-crosslinks.surge.sh

bookmark it. i add new tools every week.

if you're also building solo, reply with what you're working on. i read every reply.

— printmaxx

---

## EMAIL 5 — Day 7 (168h delay)
**Subject:** one ask
**Preview:** takes 10 seconds

you've been getting my emails for a week. you either:

a) find the tools useful
b) haven't opened a single one

if (a): forward this email to one person who'd use these tools. that's it. that's the ask. no referral link. no "share for a bonus." just forward if it's useful.

if (b): no hard feelings. unsubscribe link is below. i'd rather have 100 people who use the tools than 10,000 who don't open emails.

all tools: https://app-hub-crosslinks.surge.sh

— printmaxx

---

## IMPLEMENTATION NOTES

### ConvertKit Setup:
1. Create "Lead Magnet Signup" automation
2. Tag subscribers by source (which lead magnet they signed up from)
3. EMAIL 1 uses dynamic content: [TOOL_NAME] and [TOOL_LINK] based on signup source tag
4. Emails 2-5 are universal (same for all subscribers)
5. Set "from name" to "printmaxx" (lowercase)
6. Set reply-to: printmaxxweb@gmail.com

### Beehiiv Alternative:
1. Create automation flow with same 5 emails
2. Use "trigger: new subscriber"
3. Add delays between emails (0, 24h, 72h, 120h, 168h)
4. Enable open/click tracking
5. A/B test subject lines on emails 2-4

### FormSubmit Integration:
- Current setup sends email to printmaxxweb@gmail.com
- When ESP connected: change FormSubmit _next redirect to ESP signup URL
- OR switch to ESP's native form embed (better for automation triggers)

### Metrics to Track:
- Open rate target: >40% (email 1), >25% (emails 2-5)
- Click rate target: >8% (email 1), >4% (emails 2-5)
- Reply rate: any replies = good signal
- Unsubscribe rate: <2% per email
- Forward rate (email 5): any forwards = viral loop working
