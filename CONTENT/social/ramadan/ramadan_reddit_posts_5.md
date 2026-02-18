# Hilal Ramadan Reddit Posts (5 Posts)

Strategy: Genuine value-first. Reddit hates self-promotion. Lead with the problem, share the tool as your solution, invite feedback. Never sound like marketing.

---

## Post 1: r/islam

**Title:** I built a free bilingual (Arabic/English) Ramadan fasting tracker - looking for feedback before Ramadan starts

**Body:**

Assalamu alaikum everyone,

I wanted to share something I've been working on. Every Ramadan I'd look for a fasting tracker that works properly in Arabic for my parents, and every year the options were either English-only or had terrible Arabic support (Google Translate quality with broken RTL layout).

So I built one myself. It's called Hilal.

Here's what it does:

- **Fasting timer** - live countdown from Fajr to Maghrib based on your location
- **Prayer times** - calculated from GPS, accurate to your city
- **Quran progress tracker** - set a goal (full khatm, half, or custom) and log daily pages
- **Dua collection** - 30+ duas with Arabic text, transliteration, and English meaning
- **Taraweeh counter** - tap to count rakaat so you don't lose track
- **Last 10 nights tracker** - marks odd nights, helps plan your ibadah
- **Full Arabic/English toggle** - one tap to switch. Real RTL Arabic, not just translated buttons

It's a PWA (Progressive Web App), which means:
- No App Store download needed
- Works on any phone (iPhone, Android, anything with a browser)
- Works offline after first load
- 55KB total - loads instantly even on slow connections
- Add it to your home screen and it works like a native app

**It's completely free. No ads. No subscription. No premium tier. No data collection.** I built this as a service to the community, not a business.

Ramadan is expected to start Feb 28 or March 1 depending on moon sighting in your region. The app lets you set your start date based on your local hilal sighting.

I'd really appreciate any feedback - especially from Arabic speakers. I want the Arabic experience to feel native, not like an afterthought.

Link: [HILAL_APP_URL]

JazakAllahu khairan and may Allah accept from all of us this Ramadan.

---

**Comment Strategy:**

1. **Reply to every single comment** within 2 hours. Reddit rewards engagement.
2. If someone asks about calculation method (Hanafi vs Shafi for Asr): "Great question - Hilal currently uses [method]. I can add a toggle for calculation method if there's demand."
3. If someone asks about moon sighting vs calculation: "Hilal lets you manually set your Ramadan start date. It doesn't take a position on moon sighting vs calculation - that's for you and your community to decide."
4. If someone suggests a feature: "JazakAllahu khairan for the suggestion. Adding it to my list." (Then actually add it.)
5. If someone criticizes: Thank them sincerely. Ask for specifics. Never be defensive.
6. **Upvote every comment** on your post to boost visibility.
7. After 4-6 hours, post a follow-up comment: "Update: several people asked about [X feature]. Working on it now insha'Allah."

---

## Post 2: r/muslimtechnet

**Title:** Open source Ramadan PWA with full Arabic RTL support - built with vanilla JS, 55KB total

**Body:**

Salaam tech community,

Sharing a project I built for Ramadan - a fasting tracker called Hilal. Figured this group would appreciate the technical decisions more than the features.

**Tech stack:**
- Vanilla JavaScript (no React, no framework)
- Single HTML file PWA
- Service Worker for offline support
- CSS Grid + Flexbox for RTL/LTR layout switching
- Geolocation API for prayer time calculations
- LocalStorage for all data (zero server dependency)
- Total size: 55KB

**Why these choices:**

I wanted this to work everywhere. Not everyone has a new iPhone. Not everyone has fast internet. A 55KB PWA that works offline, loads instantly on 3G, and runs on any browser from the last 5 years covers the widest possible audience.

No framework means no build step, no dependencies to update, no security vulnerabilities from node_modules. The entire app is auditable in one file.

**Arabic RTL implementation:**

This was the hardest part. Most "bilingual" apps just flip the text direction. Real Arabic support means:
- Proper `dir="rtl"` on the document level with CSS logical properties
- Arabic typography considerations (font sizing is different for Arabic script)
- Number formatting (Arabic-Indic numerals option)
- Date formatting for Hijri calendar
- Dua text rendering with proper tashkeel (diacritical marks)

**Prayer time calculation:**

Using standard astronomical formulas. The calculation methods supported:
- Muslim World League
- Egyptian General Authority
- University of Islamic Sciences, Karachi
- Islamic Society of North America
- Umm al-Qura University, Makkah

Users pick their method. High latitude adjustments included for northern/southern locations where Fajr/Isha times can get extreme.

**What I'm looking for:**

- Code review / feedback on the Arabic implementation
- Any bugs on specific devices (especially older Android)
- Suggestions for calculation method defaults by region
- Feature requests from a technical perspective

Link: [HILAL_APP_URL]
Source: [GITHUB_URL_IF_APPLICABLE]

Happy to answer any technical questions.

---

**Comment Strategy:**

1. This subreddit values technical depth. Answer every technical question in detail.
2. If someone asks about prayer time accuracy: Share the specific formula and cite the astronomical references.
3. If someone offers a PR or code suggestion: Accept graciously, even if you don't merge it.
4. If someone suggests using a framework: Explain the size/accessibility tradeoff respectfully.
5. Post a follow-up comment with performance metrics: Lighthouse score, load time on 3G, etc.

---

## Post 3: r/Ramadan

**Title:** Free fasting timer with prayer time calculations - no ads, no sign-up, works offline

**Body:**

Assalamu alaikum and Ramadan Mubarak (almost),

With Ramadan just around the corner (Feb 28 / Mar 1 insha'Allah), I wanted to share a fasting tracker I built called Hilal.

**The problem I was solving:** During long fasting days, I kept checking multiple apps - one for prayer times, one for Quran tracking, a notes app for my dua list, and mental math for how many hours until Maghrib. I wanted everything in one place.

**What Hilal does:**

The fasting timer is the core feature. Open the app and you see one number: hours and minutes until Maghrib. That's it. When you're 10 hours into a fast and your energy is low, you just want to know how much longer. Clean. Simple. No clutter.

Beyond the timer:
- Prayer times calculated for your exact location (uses your phone's GPS)
- Quran progress tracker (set a goal, log daily pages, see if you're on pace)
- 30+ Ramadan duas with Arabic, transliteration, and English meaning
- Taraweeh rakaat counter
- Fasting streak tracker (see your consecutive days)
- Last 10 nights planner (marks odd nights for Laylatul Qadr)

**Key details:**
- Arabic and English (full bilingual, one tap to switch)
- Works offline (no internet needed after first load)
- No account creation needed
- No ads, no subscription, no premium features, completely free
- Works on any phone - just open the link and add to home screen

**About the start date:** Hilal doesn't auto-set Ramadan's start date because moon sighting varies by region. You set your own start date based on when your local community confirms the hilal (crescent moon). The app adjusts all tracking accordingly.

Link: [HILAL_APP_URL]

Would love to hear what features would make your Ramadan easier. I have two weeks before Ramadan starts and I'm still adding features.

Ramadan Mubarak to this community.

---

**Comment Strategy:**

1. r/Ramadan is smaller and more personal. Warm, conversational replies.
2. Ask commenters: "What's one thing you wish a Ramadan app had?"
3. If someone shares their Ramadan prep: Engage with their prep, not just your app.
4. Share personal Ramadan memories or goals to build rapport.
5. If someone asks about specific fiqh questions (calculation methods, etc.): "I'm a developer, not a scholar. Hilal provides the tools - please follow your local imam's guidance on fiqh matters."

---

## Post 4: r/MuslimLounge

**Title:** Ramadan prep: tools and habits I'm setting up this year

**Body:**

Salaam everyone,

Two weeks out from Ramadan and I'm trying to actually be prepared this year instead of scrambling on Day 1. Sharing my prep list in case it helps anyone else.

**Physical prep:**
- Started fasting Mondays and Thursdays to ease into it
- Adjusted bedtime by 15 minutes earlier each night (trying to be functional at Fajr)
- Meal prepped 3 soups: lentil, chicken, and tomato. Frozen in individual portions. Iftar = reheat and eat. More time for ibadah.
- Stocked up on dates, water, and suhoor staples

**Spiritual prep:**
- Wrote out my dua list (specific things I'm asking for this Ramadan)
- Started reading 2 pages of Quran daily to build the habit before going to 20/day
- Made a list of people to forgive and relationships to repair
- Set my Quran khatm goal (going for full this year insha'Allah)

**Digital prep:**
- Deleted social media apps from my phone (will reinstall after Ramadan, maybe)
- Set up screen time limits
- Installed a fasting tracker called Hilal that I've been testing - it's free, works in Arabic and English, and has prayer times, Quran tracking, and a dua collection all in one place. Honestly the bilingual feature is what sold me because I can set my mom's phone to Arabic and mine to English.
- Downloaded offline Quran audio for commutes

**The plan for the last 10 nights:**
- Took time off work for the last 5 days of Ramadan
- Planning to do itikaf at least the last 3 odd nights
- Set sadaqah reminders for every odd night

What's your prep looking like? Anything I'm missing?

---

**Comment Strategy:**

1. This is the "casual" post. Hilal is mentioned once, naturally, as part of a larger list. Not the focus.
2. Engage with everyone's prep plans. Ask questions. Be a community member first.
3. Only talk more about Hilal if someone specifically asks about it.
4. If someone shares a great tip you hadn't thought of: "Adding this to my list. JazakAllahu khairan."
5. Don't link to the app in comments unless someone asks. Let the body mention be enough.
6. Upvote and reply to every comment to boost the post in the algorithm.

---

## Post 5: r/progressive_islam

**Title:** Built a bilingual Ramadan app for my family who switches between English and Arabic constantly

**Body:**

Salaam everyone,

Wanted to share something personal I've been building. My family is split between Arabic-dominant speakers (my parents, grandparents) and English-dominant speakers (my siblings, cousins born here). Every family gathering is a mix of both languages, sometimes in the same sentence.

Every Ramadan, I'd set up my mom's phone with a fasting app. She'd call me a week later because she couldn't figure something out - the app was in English and the "Arabic mode" was basically Google Translate with broken layout. The text would overlap. Buttons would be in weird places. The Arabic font would be tiny.

So I built Hilal. It's a Ramadan fasting tracker that genuinely works in both languages.

**What "bilingual" actually means here:**

When you switch to Arabic, the entire layout flips to right-to-left. The typography is sized properly for Arabic script (Arabic characters need more vertical space than Latin characters). The diacritical marks (tashkeel) on Quran verses and duas render correctly. It doesn't just translate the words - it restructures the interface.

And when you switch back to English, everything flips back. Same data. Same tracking. Different language. One tap.

**Why this matters:**

My mom can track her fasting in Arabic. I can check her progress when she calls me and see the same data in English. My younger cousin who's learning Arabic can toggle back and forth to practice reading. My uncle who reads Arabic but prefers English UI can mix and match.

**The app itself:**

Fasting timer (Fajr to Maghrib countdown), prayer times for your location, Quran progress tracker, dua collection (Arabic + transliteration + English meaning), Taraweeh counter, last 10 nights tracker.

Free. No ads. No account needed. Works offline. Works on any phone with a browser. 55KB total.

Link: [HILAL_APP_URL]

I'm not a scholar and the app doesn't take positions on fiqh differences (calculation methods, moon sighting, etc.). It provides tools. You follow your own understanding and your community's guidance.

Would love feedback, especially from bilingual families. What would make this more useful for your household?

---

**Comment Strategy:**

1. r/progressive_islam values personal story and inclusivity. Lead with family narrative.
2. If someone raises fiqh concerns about calculation methods: "Hilal supports multiple calculation methods and doesn't default to one. I respect that different communities follow different scholarly opinions."
3. If someone asks about supporting other languages (Urdu, Turkish, Malay, etc.): "That's on my roadmap. Which language would be most useful to you?"
4. Engage warmly. This community values empathy and personal connection.
5. Avoid any language that could be perceived as gatekeeping or sectarian.
6. If someone critiques the app's approach: "Thank you for the perspective. Can you tell me more about what you'd like to see different?"
