t ha subs and # PrayerLock PWA - Deploy and Launch Playbook

**App:** PrayerLock - prayer timer, streak tracker, Qibla compass, tasbih counter
**Stack:** Single HTML file + manifest.json + sw.js (55KB total, zero dependencies)
**Status:** Built and ready to deploy
**Location:** `MONEY_METHODS/APP_FACTORY/builds/prayerlock-web/`

---

## Section 1: Deploy to Vercel (5 minutes)

### Option A: Vercel CLI

Vercel CLI is NOT currently installed. Install it first:

```bash
npm i -g vercel
```

Then deploy:

```bash
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt/MONEY_METHODS/APP_FACTORY/builds/prayerlock-web
vercel deploy --prod
```

First time will prompt you to log in and link a project. Follow the prompts. You get a `.vercel.app` URL instantly.

**Human action required:** Install Vercel CLI or use Option B/C if you prefer no CLI.

### Option B: Vercel drag-and-drop (no CLI)

1. Go to https://vercel.com/new
2. Click "Deploy" without importing a Git repo
3. Upload the `prayerlock-web` folder (all 4 files: index.html, manifest.json, sw.js, deploy.md)
4. Vercel auto-detects static site. Click Deploy.
5. Live URL in ~30 seconds.

### Option C: Netlify drop (fallback)

1. Go to https://app.netlify.com/drop
2. Drag the entire `prayerlock-web` folder onto the page
3. Done. You get a `.netlify.app` URL instantly.
4. Optional: click "Site settings" to change the subdomain name to `prayerlock.netlify.app`

### Option D: Cloudflare Pages

1. Push files to a GitHub repo: `gh repo create prayerlock --public`
2. Go to https://dash.cloudflare.com/ > Pages > Create project
3. Connect the GitHub repo
4. Build command: leave blank (static files)
5. Output directory: `.`
6. Deploy

### Custom domain setup

Buy a domain ($8-12/year). Best options:
- `prayerlock.app` - Cloudflare Registrar (cheapest renewals)
- `prayerlock.co` - Namecheap
- `prayerlock.io` - Namecheap

Point DNS to your hosting provider:
- **Vercel:** Dashboard > Project > Settings > Domains > Add domain > follow DNS instructions
- **Netlify:** Site settings > Domain management > Add custom domain
- **Cloudflare Pages:** Already on Cloudflare, just add the domain

### Post-deploy verification

After deploying to any provider, run these checks:

1. **PWA install test:** Open site on phone > browser menu > "Add to Home Screen" > verify app opens standalone
2. **Offline test:** Add to home screen > turn on airplane mode > open app > should still work
3. **Lighthouse audit:** Chrome DevTools > Lighthouse tab > check "Progressive Web App" > Run > target 90+ score
4. **Service worker:** Chrome DevTools > Application tab > Service Workers > verify "prayerlock-v1" is active
5. **Cross-browser:** Test on Safari (iOS), Chrome (Android), Firefox

---

## Section 2: Product Hunt Submission (15 minutes)

### Pre-launch checklist (1 week before)

- [ ] App deployed to production URL with HTTPS
- [ ] Take 7 screenshots (see screenshot list below)
- [ ] Record 1-minute demo video (screen record on phone, add captions)
- [ ] Create Product Hunt maker account if you don't have one
- [ ] Line up 5+ people to upvote at launch (friends, Twitter followers, Discord communities)
- [ ] Draft Twitter thread announcing the launch
- [ ] Optional: buy custom domain and point it

### Screenshots needed

Capture at 780x1688 minimum (2x iPhone 14 Pro). Use Chrome DevTools > Toggle device toolbar > iPhone 14 Pro.

1. Timer screen with prayer in progress, circular countdown at ~60%, dark mode
2. Streak view with filled contribution graph showing 14+ day streak
3. Qibla compass with arrow pointing toward Mecca, bearing degrees visible
4. Tasbih counter mid-count (21/33), ripple effect visible
5. Daily verse banner with share button on timer screen
6. Light mode view of any screen
7. "Add to Home Screen" browser prompt

### Submission copy

**Product name:** PrayerLock

**Tagline:** The prayer timer that builds streaks, not guilt

**Short description:**
PrayerLock helps you build a consistent prayer habit. Set a timer, track your streak, find Qibla direction, and count tasbih. Works offline. No account needed. Your data stays on your device.

**Full description:**

Building a prayer habit is hard. Existing apps are bloated, require accounts, or push premium subscriptions before you start.

PrayerLock is a focused prayer companion with just what you need:

- Prayer Timer: 5-60 minutes, circular countdown, gentle completion sound, optional nature/rain background
- Streak Tracker: GitHub-style contribution graph. Milestones at 7, 14, 30, 60, 90 days. The streak keeps you going.
- Qibla Compass: Uses your phone's compass and GPS to point toward Mecca. Works anywhere.
- Tasbih Counter: Digital prayer bead counter with haptic feedback. Presets (33, 99) or custom.
- Daily Verse: One inspirational verse each day from the Quran and Bible.

No account required. Works offline (PWA). All data stored locally. Interfaith (Muslim + Christian). Free. No ads.

55KB single HTML file. Zero dependencies. Just open it and pray.

**Topics/tags:** Productivity, Wellness, Open Source, Progressive Web App

**Links:**
- Website: [YOUR_DEPLOY_URL]
- GitHub: [CREATE_AND_LINK_REPO]

### First comment (maker comment)

Post this immediately after submitting:

```
Hey PH! I'm the maker of PrayerLock.

I built this because I wanted a prayer companion that respects my time and privacy. Every prayer app I tried either wanted my email before I could use it, or pushed a $9.99/month subscription for basic features.

PrayerLock is:
- A single HTML file (55KB)
- Works offline after first load
- Zero accounts, zero tracking, zero ads
- Interfaith (Quran + Bible daily verses)

The streak tracker is what keeps me consistent. Seeing that green grid fill up day by day is surprisingly motivating.

Tech: Vanilla HTML/CSS/JS, TailwindCSS via CDN, Service Worker for offline, localStorage for all data. No build step, no framework, no backend.

Would love your feedback. What features would make your prayer practice better?
```

### Optimal launch timing

- **Best days:** Tuesday, Wednesday, Thursday
- **Submit at:** 12:01 AM Pacific Time (to maximize the full 24-hour voting window)
- **Avoid:** Mondays (competition from weekend builders), Fridays (lower traffic), weekends

### Upvote strategy

1. DM 5-10 friends/followers BEFORE launch day. Ask them to upvote + leave a comment at 12:01 AM PT
2. Post the PH link on your Twitter immediately after submission
3. Share in relevant Discord servers (Muslim tech, indie hackers, build in public)
4. Reply to EVERY comment within 1 hour
5. Post updates throughout the day (engagement signals to PH algorithm)

---

## Section 3: Directory Submissions (30 minutes)

### Priority submission list (top 20 for PWAs)

Submit in this exact order. Higher priority directories first.

#### Tier S: Submit day of launch (highest traffic)

**1. Product Hunt** - producthunt.com
- Steps: Sign up as maker > Submit product > Add screenshots, tagline, description, first comment
- Copy: Use "Submission copy" from Section 2
- Notes: Launch Tuesday-Thursday at 12:01 AM PT

**2. Hacker News (Show HN)** - news.ycombinator.com
- Steps: Submit as "Show HN: PrayerLock - prayer timer PWA, single HTML file, works offline"
- URL: Link directly to live app
- Copy: Keep it technical. "55KB single HTML file. Vanilla JS. Service worker for offline. No framework, no backend, no account."
- Notes: HN audience loves minimal, no-nonsense tools. Lean into the "single file PWA" angle.

**3. Reddit r/SideProject** - reddit.com/r/SideProject
- Steps: Create post with title "I built a prayer timer PWA that works offline (55KB, no account needed)"
- Copy: Explain the build, share lessons learned. Include link. Be genuine, not promotional.
- Notes: Most launch-friendly subreddit. High conversion.

**4. Reddit r/InternetIsBeautiful** - reddit.com/r/InternetIsBeautiful
- Steps: Submit link with descriptive title
- Notes: 17M members. Very selective. If it gets traction, massive traffic. Worth the shot.

#### Tier A: Submit within first week

**5. IndieHackers** - indiehackers.com
- Steps: Create new product listing > Share as milestone post "Just launched PrayerLock"
- Copy: Focus on the build story and what you learned

**6. BetaList** - betalist.com
- Steps: Submit at betalist.com/submit > Fill in product details
- Approval: 3-7 days
- Copy: Use short description from Section 2

**7. DevHunt** - devhunt.org
- Steps: Submit product > Add GitHub link (create public repo first)
- Notes: Dev-focused PH alternative. Good for technical PWA angle.

**8. Reddit r/webdev** - reddit.com/r/webdev
- Steps: Post about the technical build. "I built a full PWA in a single HTML file"
- Copy: Technical details. Service worker caching, offline-first, no framework choice.

**9. Reddit r/islam** - reddit.com/r/islam
- Steps: Post as genuine community contribution. "Built a free prayer timer with Qibla compass"
- Copy: Focus on the prayer features, not the tech. Be respectful.

**10. Reddit r/productivity** - reddit.com/r/productivity
- Steps: Post about habit tracking angle. "I built a prayer streak tracker with GitHub-style contribution graph"
- Copy: Focus on the streak/habit mechanics

**11. Reddit r/Christianity** - reddit.com/r/Christianity
- Steps: Post about the interfaith angle. "Made a free prayer companion app"
- Copy: Focus on daily Bible verses and prayer timer features

**12. Reddit r/buildinpublic** - reddit.com/r/buildinpublic
- Steps: Share build journey and launch day post

#### Tier B: Submit within first 2 weeks

**13. Reddit r/SaaS** - reddit.com/r/SaaS
- Steps: Share as launch announcement
- Notes: SaaS-focused, but free tools still welcome

**14. Reddit r/Solopreneur** - reddit.com/r/Solopreneur
- Steps: Share as solopreneur build story

**15. Reddit r/EntrepreneurRideAlong** - reddit.com/r/EntrepreneurRideAlong
- Steps: Case study format. "How I built and launched a PWA in a weekend"

**16. PeerList** - peerlist.io
- Steps: Add to your PeerList portfolio as a project

**17. Reddit r/indiehackers** - reddit.com/r/indiehackers
- Steps: Share milestone and lessons

**18. Reddit r/MuslimLounge** - reddit.com/r/MuslimLounge
- Steps: Share as community resource. "Free prayer companion app, no account needed"

#### Tier C: Submit within first month (backlinks + long tail)

**19. PWA directories**
- https://www.pwa.rocks/ - Submit PWA
- https://appsco.pe/ - Submit as web app
- https://pwa-directory.appspot.com/ - Google's PWA directory

**20. Smaller directories (batch submit)**
Submit to these in one sitting. Copy-paste the same description:
- Fazier (fazier.com)
- Garage.dev (garage.dev)
- tinystartups (tinystartups.com)
- TinyLaunch (tinylaunch.co)
- ShipYard HQ (shipyard.live)
- RankInPublic (rankinpublic.com)

### Reddit posting rules

- Space submissions 24-48 hours apart (don't carpet-bomb all subreddits on the same day)
- Customize the title and angle for each subreddit
- Reply to every comment
- Don't cross-post the same link repeatedly. Write fresh posts.
- If a post gets removed, don't repost. Move to the next subreddit.

---

## Section 4: PrayerLock to Gumroad cross-sell

### Add Gumroad product link to PrayerLock

After deploying, add a subtle upsell inside the app. Two options:

**Option A: Settings page link**
Add a "Premium Prayer Journal (PDF)" link in the settings tab that opens a Gumroad product page.

**Option B: Post-milestone prompt**
After hitting a streak milestone (7 days, 14 days), show a congratulations modal with: "Want to go deeper? Get the Premium Prayer Journal - 30 days of guided prayer reflections. [Get it on Gumroad]"

### "Premium Prayer Journal" Gumroad product concept

**Product:** 30-Day Premium Prayer Journal (PDF + Notion template)
**Price:** $4.99 (impulse buy price point)
**Contents:**
- 30 daily guided prayer prompts (interfaith)
- Reflection questions for each day
- Gratitude section
- Scripture/verse highlights
- Weekly review pages
- Printable or use in Notion

**Gumroad listing copy:**
"You've built the habit. Now go deeper. 30 days of guided prayer reflections, designed to complement PrayerLock. Daily prompts, scripture highlights, and space for gratitude. PDF + Notion template. Print it or use it digital."

**Create at:** gumroad.com > New product > Digital product > Upload PDF + Notion template link

### Social cross-promotion

**@daily_anchor_faith** (faith niche account):
- Pin a tweet: "I built PrayerLock - free prayer timer with streak tracking. No ads, no account, works offline. [link]"
- Weekly prayer habit tips that reference PrayerLock features
- Share user streaks and milestones (with permission or anonymized)
- Link to Gumroad journal in bio

**Content ideas for @daily_anchor_faith:**
1. "Day 7 of my prayer streak. Here's what changed."
2. "The Qibla compass in PrayerLock just works. No account, no BS."
3. "33 tasbih before bed. Simple. Try it tonight."
4. "Your prayer streak is more motivating than any alarm app."
5. "Built a prayer timer because every existing one wanted my email first."

---

## Section 5: Biomaxx app status

**Location:** `MONEY_METHODS/APP_FACTORY/builds/biomaxx-sdk54/`
**Status:** NOT deployable. Directory contains only documentation files:
- `APP_STORE_SUBMISSION_CHECKLIST.md` (19KB)
- `LAUNCH_ASSETS.md` (16KB)

No source code, no built app. The biomaxx app needs to be built before deployment. This is a React Native / Expo app that requires:
1. Full code implementation
2. Expo build (`eas build`)
3. App Store submission (Apple Developer account required, $99/year)

**Action:** Biomaxx is not ready for deployment. Focus on PrayerLock launch first. Biomaxx is a separate build sprint.

---

## Launch day timeline (suggested)

**Night before (11 PM PT):**
- Final check: app loads, PWA installs, offline works
- Screenshots ready, video ready, PH listing drafted
- DM 5 friends: "upvoting tomorrow at midnight PT, here's the link"

**12:01 AM PT - Launch:**
- Submit to Product Hunt
- Post maker comment immediately
- Tweet the PH link with launch thread

**6:00 AM PT:**
- Submit to Hacker News (Show HN)
- Post on r/SideProject
- Share on IndieHackers

**12:00 PM PT:**
- Post on r/islam, r/Christianity
- Share on r/webdev (technical angle)
- Reply to all PH comments

**6:00 PM PT:**
- Post on r/productivity
- DM 10-20 relevant Twitter accounts
- Share in Discord communities

**Day 2:**
- Submit to BetaList, DevHunt, PeerList
- Post on r/buildinpublic
- Write "How I built PrayerLock" Twitter thread

**Day 3-7:**
- Submit to remaining Reddit subs (one per day)
- Submit to PWA directories
- Batch submit to smaller directories

**Day 7-30:**
- Write blog post for Dev.to
- Create Gumroad product (Premium Prayer Journal)
- Add Gumroad link to PrayerLock settings
- Start @daily_anchor_faith content


---

## Pending Enhancement (ALPHA6695, Score: 24)

**Source:** ProductHunt | **URL:** https://www.producthunt.com/products/jdoodle-ai
**Added:** 2026-02-18T07:12:19-05:00

[PH LAUNCH] JDoodle.ai MCP: Build and deploy web apps straight from ChatGPT/Claude

