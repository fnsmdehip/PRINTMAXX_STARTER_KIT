---
subreddit: r/SideProject
title: "launched 3 apps this month with $0 in hosting costs. here's the exact free stack."
flair: Show & Tell
scheduled_date: 2026-03-12
---

I keep seeing posts about "what's the cheapest way to host my side project" so here's mine: literally free.

not free trial. not "free for 12 months." actually free, indefinitely.

the stack:

- **hosting:** surge.sh (unlimited free projects, custom domains, SSL included)
- **database:** localStorage + IndexedDB (client-side, no server needed)
- **auth:** none yet (MVP stage - keeping it simple)
- **analytics:** self-built 14-line tracker that logs to a JSON file
- **CI/CD:** a bash script that runs `surge ./dist` in 2 seconds
- **design:** system fonts + hand-written CSS (no Tailwind, no Bootstrap)
- **icons:** single SVG per app, designed in Figma free tier

total monthly cost: $0.00. I checked.

I launched 3 apps this month using this stack:

1. a prayer time tracker (PWA that works offline)
2. a workout timer with custom intervals
3. a daily focus app that blocks you from using it after you complete your task

all three are under 50KB total. they load in under 1 second on 3G. they work offline. they're installable on any device.

the "why" behind going this extreme:

I have exactly $0 in runway. I'm pre-revenue. every dollar I spend on infrastructure before having users is a dollar I can't spend on distribution. so I optimized for zero cost until I have paying customers.

the tradeoffs are real though:

- no server means no user accounts (yet). data lives on device.
- no database means if someone clears their browser data, their progress is gone.
- no framework means I write more boilerplate code upfront.
- no analytics service means my usage data is basic.

but here's the thing: none of my apps need user accounts at MVP stage. a prayer timer doesn't need a login. a workout timer doesn't need cloud sync. a focus app works better with local data because it's private by default.

I'll add server-side features when I have users who ask for them. until then, $0/month.

anyone else running a completely free stack? curious what other approaches people are using.
