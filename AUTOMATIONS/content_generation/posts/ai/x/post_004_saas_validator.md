# Post 004 — SaaS Validation Loop

**Platform:** X (Twitter)
**Length:** Thread (5 tweets)
**Niche:** AI / Automation

---

spent last week automating SaaS idea validation. fed 150 startup ideas through claude api. scored on 7 dimensions: market_size, founder_capital, competition, time_to_revenue, automation_potential, moat_strength, downside_risk.

results: 8 ideas scored 7.2+/10. everything else under 6. typical investor scores 2-3 ideas per week manually. this does 150 in 30 minutes.

the formula is stupid simple:
- idea name + description + target market
- claude scores on 7 rubrics
- outputs a csv
- use only 7.2+ ideas for building
- everything under 6.0 is noise

saves 60 hours of founder deliberation per month. most teams waste this time arguing about vibes.

i'm selling the scorer (it's 180 lines of python + one claude call) as a $29 digital product. zero customer acquisition. just post it on twitter and let it compound.

time to first $ = this week (already have 3 interested). no stripe account needed yet, just gumroad. that's the actual micro-saas meta right now.

---
