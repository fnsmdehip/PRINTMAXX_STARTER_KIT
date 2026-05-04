# Response Template: Polymarket Trading Bot - $400

**Opportunity ID:** FP-002
**Source:** r/forhire
**URL:** https://reddit.com/r/forhire/comments/1r44um0/hiring_looking_for_python_developer_to_build/
**Author:** u/EtikDigital512
**Budget:** $400
**Age:** ~3 hours
**Score:** 70 (HOT)
**Matched Fiverr Gig:** GIG 5 - Web Scraper / Data Extraction (closest match for Python automation work)

---

## What They Want

Python developer to build an automated trading bot for Polymarket (prediction market). $400 budget. This is a straightforward Python automation project.

## Our Edge

We can build a Polymarket API integration in a few hours. The CLOB API is well-documented. $400 for what takes us 2-3 hours of work.

---

## Reddit Response (COPY-PASTE READY)

```
interested in this. i've built Python automation tools and API integrations for trading platforms before.

some questions to scope this properly:

1. are you looking at the CLOB (central limit order book) API or the simpler market API?
2. what's the strategy? basic market making, conditional orders, event-driven trades, or something custom?
3. do you need a web dashboard to monitor it, or is CLI/terminal output fine?
4. hosting preference? (your own server, AWS, or do you need me to set that up too?)
5. any risk management rules you want baked in? (max position size, stop losses, daily limits)

i can build the core bot (API auth, order placement, position tracking, basic strategy execution) within 3-5 days. happy to share a quick architecture diagram before we start so you know exactly what you're getting.

the Polymarket CLOB API is pretty clean. main considerations are rate limiting, websocket vs polling for price updates, and handling the gas fees on Polygon for settlement.

DM me if you want to talk details.
```

---

## DM Follow-Up

```
hey, thanks for the interest.

here's how i'd structure the $400 budget:

phase 1 ($200): core bot
- polymarket API authentication
- market data fetching (prices, volumes, order book)
- order placement (buy/sell limit and market orders)
- position tracking and P&L monitoring
- basic logging

phase 2 ($200): strategy + deployment
- your specific trading strategy coded in
- risk management (position limits, loss limits)
- deployment script (can run on any Linux server or your local machine)
- documentation on how to modify parameters

deliverables: full source code, requirements.txt, README with setup instructions, and a 30-minute walkthrough call if needed.

timeline: 4-5 days from start to delivery.

i'll also include a simple config file so you can adjust strategy parameters without touching code.

want to hop on a quick call to discuss the strategy specifics?
```

---

## Technical Prep Notes

- Polymarket CLOB API docs: https://docs.polymarket.com/
- Python packages needed: py-clob-client, web3, requests
- Consider building a reusable template we can sell on Fiverr as "custom trading bot" gig
