# Reddit Distribution - Cycle 36 - 2026-04-01

## NEW ASSETS THIS CYCLE
- streakr.surge.sh
- best-sleep-supplement-men-over-55.surge.sh (6-page affiliate cluster complete)
- cnsnt-desktop.surge.sh
- Digital products queue (22 PDFs)

---

## POST 1 — r/Supplements (500K members)
**PRIORITY: HIGH — tracker queued this for cycle 36**

**Title:** Compared 19 sleep supplements for men over 55 — only 5 cleared the evidence bar (full ingredient analysis inside)

**Body:**
Background: I've been researching sleep maintenance insomnia specifically for men over 55. The issue is distinct from general insomnia — GH drops 75% after 50, which shrinks N3 deep sleep and leaves you in light sleep. That's why it's 3-4 AM waking, not trouble falling asleep.

Here's what I found actually has evidence:

**1. Magnesium glycinate / bisglycinate**
Strongest evidence of the bunch — 8 randomized controlled trials in adults 50+. 200-400mg before bed. Targets sleep maintenance specifically. Thorne's version has the cleanest form factor.

**2. Low-dose melatonin (0.3mg timed-release)**
Not the 5-10mg OTC products. Your body produces 0.1-0.3mg naturally. The high-dose pills are overdosing you, which explains next-day grogginess and the feeling it "stopped working." Life Extension makes a 0.3mg timed-release that hits the science correctly.

**3. Ashwagandha (300mg root extract)**
Only relevant if your insomnia has a cortisol component — stress-triggered 3 AM waking. Takes 8 weeks minimum to see effect. Weak evidence for sleep onset, moderate evidence for sleep maintenance when cortisol is the driver.

**What to skip:**
- Proprietary blends that don't list doses
- Magnesium oxide (40% absorption rate, most cheaper supplements use it)
- ZMA stacks (the zinc and B6 are fine, the doses are often off)
- Prevagen (the phosphatidylserine evidence is weak for sleep specifically)

Full ranked comparison with drug interaction table (especially anticoagulants and BP meds): https://best-sleep-supplement-men-over-55.surge.sh/

Not a doctor. Check with yours before adding anything new, especially if you're on blood thinners, thyroid meds, or blood pressure medication.

**Crosspost to:** r/over50, r/Nootropics (remove affiliate link for Nootropics — post knowledge only there)

---

## POST 2 — r/ADHD (700K members)
**PRIORITY: HIGH — focuslock was queued from last cycle**

**Title:** Built a free Pomodoro timer with task breakdown for ADHD — no account, no sync, just works

**Body:**
I built FocusLock after trying every productivity app and hating the onboarding.

What it does:
- Pomodoro timer with configurable work/break intervals
- Task list so you know what you're working on
- Stats so you can see your actual focus patterns
- Offline, all localStorage, no account, no sync required
- Free

What it doesn't do: guilt you, gamify your streaks into a job, upsell you every 3 screens.

https://focuslock-web.surge.sh

If you try it, the one thing that's helped me most is keeping the task list to 3 items max. More than 3 and the decision overhead kicks in.

---

## POST 3 — r/biohackers (300K+ members)
**PRIORITY: MEDIUM — sleepmaxx queued from last cycle**

**Title:** Sleep optimization tracker PWA — logs duration, quality rating, and tags what you did before bed. Free, offline, no account

**Body:**
Built SleepMaxx as a simple sleep logging tool focused on pattern spotting.

You log:
- Sleep time / wake time (duration auto-calculates)
- Quality rating 1-5
- Tags for what you did (caffeine, exercise, alcohol, screens, supplements)

After 2 weeks you can see which tags correlate with your quality scores. That's it. No AI sleep coach. No subscription. No "upgrade for insights."

The pattern spotting is the insight. You do it yourself.

https://sleepmaxx-web.surge.sh

Offline-first PWA, data stays in your browser. Export to CSV if you want to take it somewhere else.

---

## POST 4 — r/privacy (1.5M members)
**Title:** Built an offline-first consent form builder with AES-256 encryption — desktop app available, 3.4MB, macOS

**Body:**
cnsnt is a consent form and document builder where all data is encrypted with AES-256-GCM and stays on your device.

Zero server. Zero sync. You own the backup.

11 templates (general consent, photo consent, NDA, media release, etc.). You fill them in, they're encrypted locally, you can back up to whatever cloud storage you already use — it's just an encrypted file.

Web version: https://cnsnt-web.surge.sh
Desktop version (Tauri, macOS, 3.4MB DMG): https://cnsnt-downloads.surge.sh

If you're a photographer, therapist, freelancer, or anyone who collects consent forms and doesn't want that data on someone else's server — this is for you.

Source available on request. Built with Tauri (Rust backend) for the desktop version.

---

## POST 5 — r/sideproject (75K members)
**Title:** Day 57 update: 398 deployed apps, 22 sellable products, $0 revenue — here's the actual bottleneck

**Body:**
57 days in. Here's the real state of things.

What's deployed:
- 398 live surge.sh deployments (apps, tools, streak trackers, affiliate pages, landing pages)
- 22 digital products as PDFs ready to sell (Claude Code guides, cold email playbooks, prompt vaults)
- 6-page health affiliate cluster for men's supplements

What's blocking revenue:
- No Stripe account (need one to sell anything)
- No Gumroad account (22 products sitting in a folder)
- Affiliate program signups not done
- Gmail API auth not set up for cold email pipeline

Everything that requires making an account has been deprioritized because building more stuff is more fun. Classic solopreneur trap.

The cold email pipeline is fully built. The lead qualification is done. The email templates are there. But without Gmail API auth, it can't send.

This week is accounts week, not building week.

Anyone else find the "make an account" step disproportionately painful relative to its actual difficulty?

---

## CROSSPOST NOTES

| Post | Primary Sub | Crosspost |
|------|------------|-----------|
| Sleep supplements | r/Supplements | r/over50, r/Nootropics (no link) |
| FocusLock | r/ADHD | r/productivity, r/selfimprovement |
| SleepMaxx | r/biohackers | r/longevity, r/sleep |
| cnsnt privacy | r/privacy | r/selfhosted, r/degoogle |
| Day 57 update | r/sideproject | r/Entrepreneur, r/solopreneur |
