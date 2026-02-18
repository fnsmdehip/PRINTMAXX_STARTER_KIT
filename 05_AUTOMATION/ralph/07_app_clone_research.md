# Ralph Task: App Clone Research

Find successful apps, clone for niche audiences, add cute mascot, ship fast.

**Strategy Source:** "Find app making $100k/mo → build your version → niche target → add pet mascot → launch"

---

## Context
- Read `LEDGER/APP_FACTORY_METHODS.csv` for existing app ideas
- Read `MONEY_METHODS/APP_FACTORY/` for specs and playbooks
- Output findings to `LEDGER/APP_CLONE_OPPORTUNITIES.csv`
- Use MIT-licensed repos when possible for faster builds

## Success Criteria

### Step 1: Find $100k+/mo Apps
1. [ ] Check app revenue trackers (appfigures, sensortower estimates)
2. [ ] Search Product Hunt for trending utility apps
3. [ ] Check App Store top charts (Productivity, Health, Lifestyle)
4. [ ] Monitor indie hacker success stories
5. [ ] Check r/SideProject, r/startups for revenue posts

### Step 2: Analyze Winning Apps
For each candidate app:
6. [ ] Document monthly revenue (estimated)
7. [ ] Identify core mechanic (what does it actually do?)
8. [ ] Note pricing model (freemium, subscription, one-time)
9. [ ] Analyze App Store reviews (what do users love/hate?)
10. [ ] Check for open-source alternatives on GitHub

### Step 3: Find Niche Angles
11. [ ] List underserved audiences for each app:
    - For women
    - For gym bros / fitness
    - For Christians / faith
    - For vegans / specific diets
    - For parents / families
    - For students
    - For remote workers
    - For specific professions
12. [ ] Validate niche has demand (subreddit size, hashtag volume)
13. [ ] Check if niche version already exists

### Step 4: Find MIT-Licensed Repos
14. [ ] Search GitHub for open-source versions
15. [ ] Filter by MIT, Apache 2.0, or BSD licenses (can use commercially)
16. [ ] Assess code quality and activity
17. [ ] Note what customization needed
18. [ ] Document repo URL and license

### Step 5: Design Niche Version
19. [ ] Pick winning app + niche combination
20. [ ] Design mascot/character (cute = higher retention)
21. [ ] Plan niche-specific features
22. [ ] Outline MVP scope (what's minimum to ship?)
23. [ ] Estimate build time

## MIT/Open Source Search Strategy

Search GitHub with these patterns:
```
# Find alternatives to popular apps
"{app name} clone" license:mit
"{app name} alternative" license:mit
"open source {app category}" license:mit

# Find starter templates
"react native {app type}" license:mit
"flutter {app type}" license:mit
"nextjs {app type}" license:mit

# Specific categories
"habit tracker" license:mit stars:>100
"screen time" license:mit
"meditation app" license:mit
"workout tracker" license:mit
```

## Output Format

### APP_CLONE_OPPORTUNITIES.csv
```csv
id,original_app,revenue_estimate,core_mechanic,niche_angle,mascot_idea,mit_repo,repo_url,build_estimate,priority
1,Opal,$600k/mo,screen blocker,faith (PrayerLock),praying hands emoji,yes,github.com/...,2 weeks,HIGH
```

### For each high-priority opportunity, create:
```markdown
# Clone Opportunity: [App Name] for [Niche]

## Original App
- Name:
- Revenue:
- Core mechanic:
- Why it works:

## Niche Version
- Target audience:
- Niche-specific angle:
- Mascot/character:
- Unique features:

## Technical Approach
- MIT repo to fork: [URL]
- License: MIT/Apache/BSD
- Code quality: Good/Medium/Needs work
- Customization needed:

## MVP Scope
- Must have:
- Nice to have:
- Cut for v1:

## Launch Plan
- Build time:
- Launch channel:
- Content hooks:
```

## Known Winners to Research

### Screen Time/Blocker Apps ($100k-600k/mo)
- Opal - $600k/mo
- BePresent - $300k/mo
- Brainrot - $100k/mo
- One Sec - $200k/mo

### Habit/Streak Apps
- Streaks
- Habitica
- Loop Habit Tracker (open source!)

### Wellness/Meditation
- Calm
- Headspace
- Insight Timer

### Fitness
- Strong
- Hevy
- JEFIT

## Constraints
- Only use MIT, Apache 2.0, BSD, or similar permissive licenses
- GPL requires releasing your code - avoid unless willing
- Always check license file in repo
- Credit original authors per license requirements

## After Completion
- Update `LEDGER/APP_CLONE_OPPORTUNITIES.csv`
- Create detailed specs in `MONEY_METHODS/APP_FACTORY/clone_opportunities/`
- Update `.ralph/progress.md`

---

test_command: "cat LEDGER/APP_CLONE_OPPORTUNITIES.csv | wc -l"
