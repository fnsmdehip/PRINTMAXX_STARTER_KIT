# Pipeline Building-in-Public Content — 2026-02-17

Generated from real pipeline metrics. @PRINTMAXXER voice.
Status: PENDING_REVIEW

## Tweets (pick 1-2 per day)

### Tweet 1
```
most people manually find leads one at a time. I downloaded 2.87 million from Overture Maps, deduped to 1.45M unique domains, and built a closed-loop pipeline that qualifies → emails → tracks automatically. 7,799 hot leads so far.
```

### Tweet 2
```
analyzed 83,200 business websites last night while sleeping. 7,799 have garbage sites that need rebuilding. cold emails already drafted. this is what automation looks like.
```

### Tweet 3
```
built a system that scores websites 0-100 on design, SEO, and AI readiness. ran it against 83,200 local businesses. 9.4% scored as hot prospects. cold outreach pipeline generates emails while I sleep.
```

## Thread (7 tweets)

### 1/7
```
I built a system that finds local businesses with garbage websites and cold emails them with live demos of what their site COULD look like. here's exactly how it works (and the numbers so far). 🧵
```

### 2/7
```
step 1: data.

downloaded 2.87 million US business locations from Overture Maps (free, open data). dentists, lawyers, realtors, gyms, salons, restaurants, chiropractors, vets, plumbers.

filtered to 1.45 million unique domains after dedup.
```

### 3/7
```
step 2: website analysis.

each site gets scored 0-100 across 5 dimensions:
• design modernity (CSS Grid vs table layouts)
• SEO quality (meta tags, schema, sitemap)
• AI/GIO readiness (structured data, FAQ content)
• mobile responsiveness
• business activity signals

runs at ~12 sites/second with 30 parallel workers.
```

### 4/7
```
step 3: automatic cold email generation.

hot leads (score >= 65) get personalized 3-email sequences. each email includes a live demo URL matching their industry. dental practice → dental-demo.surge.sh. law firm → legal-demo.surge.sh.

the demo sites are already live. 16 of them.
```

### 5/7
```
step 4: closed loop.

entire pipeline runs via cron at 3am. crash recovery built in (active-tasks.md pattern from OpenClaw). if it dies mid-batch, next run picks up exactly where it left off.

qualify → email → track → repeat. no human in the loop.
```

### 6/7
```
current numbers:

• 83,200 websites analyzed (of 1.45M)
• 7,799 hot leads identified
• 432,360 cold emails generated
• 16 live demo sites
• 6 industry templates

total cost: $0 (Overture Maps is free, surge.sh is free, email via smtplib).
```

### 7/7
```
the playbook:

1. find businesses with bad websites (automated)
2. show them what a good one looks like (live demos)
3. offer to build it for $500-$3,000
4. use AI tools to actually build it in 2 hours

margin is insane because the build cost is near zero.

shipping > planning.
```
