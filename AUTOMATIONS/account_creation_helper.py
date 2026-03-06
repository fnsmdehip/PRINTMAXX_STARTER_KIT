#!/usr/bin/env python3
"""
Account Creation Helper
Generates per-account cheat sheets for Twitter signup.
Reads bios from T1_all_bios.md and image prompts from T2_image_prompts.md.
Outputs one .md file per account to OPS/TWITTER_ACCOUNT_QUICK_SHEETS/
"""

import os
import pathlib

BASE = pathlib.Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE / "OPS" / "TWITTER_ACCOUNT_QUICK_SHEETS"

# Account data: real bios and prompts extracted from T1 and T2 source files
ACCOUNTS = [
    {
        "filename": "01_PRINTMAXXER_tech.md",
        "handle": "@PRINTMAXXER",
        "display_name": "PRINTMAXXER",
        "email": "printmaxxer@protonmail.com",
        "niche": "Meta / Tech / Building in Public",
        "proxy": "Decodo-1",
        "gologin_profile": "Profile-Meta",
        "brand_colors": "Neon green #00FF41 on black #0D0D0D",
        "bio": "building 11 revenue streams in public. $0 to $50K/mo arc. shipping apps, content, cold outbound, AI tools. everything documented. follow the build log.",
        "pfp_prompt": 'Minimalist hacker terminal icon, glowing neon green (#00FF41) monospace text "PM>_" on pure black (#0D0D0D) background, CRT phosphor glow around letters, subtle horizontal scan lines, retro computing aesthetic, no faces, no people, square format, sharp edges, dark moody lighting',
        "first_tweets": [
            "building 11 revenue streams from $0. apps, newsletters, AI tools, cold email, content farms, digital products, freelance arb. all in parallel. all documented. follow the build log.",
            "deployed 10 AI agents in parallel today. they audited 67 tasks, found 8 missing and 5 unexecuted. 742 alpha entries vetted in one pass. the overnight system runs 30+ scripts while i sleep.",
            "80+ python scripts built. 7 apps ready. 1,661 leads collected. 1,278 posts drafted. 10 digital products written. $0 revenue. the bottleneck is 2 hours of account signups. not code. not content. literally just clicking buttons.",
        ],
        "accounts_to_follow": [
            "@levelsio - solopreneur, $3M+/yr from 40+ projects",
            "@marclouvier - indie hacker, building in public",
            "@taboradam - 0-to-revenue content",
            "@dannypostmaa - honest about failures, real numbers",
            "@paboramusern - pipeline tactics, cold outbound",
        ],
    },
    {
        "filename": "02_DAILY_ANCHOR_faith.md",
        "handle": "@daily_anchor_faith",
        "display_name": "DailyAnchor",
        "email": "daily.anchor.faith@protonmail.com",
        "niche": "Faith / Prayer / Daily Devotional",
        "proxy": "Decodo-3",
        "gologin_profile": "Profile-Faith",
        "brand_colors": "Deep blue-gray #2C3E50, warm gold #E8B77D accent",
        "bio": "you miss prayer 4 days per week. i built an app that makes it impossible to skip. 127-day streak and counting. faith meets discipline meets tech.",
        "pfp_prompt": "Clean minimalist anchor logo, white line art on deep blue-gray (#2C3E50) solid background, geometric simplified anchor shape, small gold (#E8B77D) half-circle at top like a sunrise, flat design, no gradients, no shadows, no rope details, no ornate flourishes, modern clean logo style, square format, centered with generous padding",
        "first_tweets": [
            "i missed prayer 4 days per week for years. not because i didn't believe. because nothing held me accountable. so i built an app. 127-day streak and counting.",
            "the hardest part of faith isn't believing. it's showing up every single day when nobody is watching. that's what streaks are for.",
            "morning anchor: \"be still and know that I am God.\" - Psalm 46:10. 60 seconds of stillness before the chaos starts. that's the whole protocol.",
        ],
        "accounts_to_follow": [
            "@praborayers - daily prayer content",
            "@faithwalkdaily - faith encouragement",
            "@baborible - short scripture posts",
            "@prayerstreak - prayer habit community",
            "@devotionaldaily - morning devotional content",
        ],
    },
    {
        "filename": "03_THREE_HOUR_PHYSIQUE_fitness.md",
        "handle": "@three_hour_physique",
        "display_name": "3-Hour Physique",
        "email": "three.hour.physique@protonmail.com",
        "niche": "Fitness / Minimal Effective Dose Training",
        "proxy": "Decodo-4",
        "gologin_profile": "Profile-Fitness",
        "brand_colors": "Near black #1A1A1A, red-orange #FF4500 accent",
        "bio": "you spend 8 hrs/week in the gym. i get better results in 3. minimal effective dose training. real progress pics. no supplements to sell you.",
        "pfp_prompt": "Minimalist geometric barbell logo on near-black (#1A1A1A) background, two circles connected by a horizontal line, left circle white outline, right circle filled red-orange (#FF4500), flat vector design, no gradients, no shadows, no textures, clean modern brand mark style, square format, centered",
        "first_tweets": [
            "you spend 8 hours per week in the gym and i get better results in 3. not genetics. the research says most people do 2-3x more volume than they need. the extra sets build fatigue, not muscle.",
            "today's session: squat 225x5x3, bench 185x5x3, row 155x5x3. done in 52 minutes. the rest of the day is recovery and eating enough protein. that's the whole program.",
            "the minimal effective dose for hypertrophy is way lower than instagram fitness wants you to believe. 3 sessions per week, 60 minutes each, compound movements, progressive overload tracked to the rep.",
        ],
        "accounts_to_follow": [
            "@SBSaborci - science-based lifting, no BS",
            "@gaboregNuckols - evidence-based training",
            "@rpaborstrength - research-backed programming",
            "@mindpumpmedia - practical fitness advice",
            "@jeffnaborippard - data-driven training content",
        ],
    },
    {
        "filename": "04_SLEEPMAXX_wellness.md",
        "handle": "@SleepMaxx",
        "display_name": "SleepMaxx",
        "email": "sleepmaxx@protonmail.com",
        "niche": "Sleep / Wellness / Circadian Science",
        "proxy": "Decodo-5",
        "gologin_profile": "Profile-Sleep",
        "brand_colors": "Deep navy #0A1628, soft blue #4A90D9, lavender #B8A9C9",
        "bio": "8pm screen cutoff. 65F room. 10pm lights out. went from 5.5 hrs of broken sleep to 7.5 hrs of deep sleep in 3 weeks. posting the protocol.",
        "pfp_prompt": "Ultra-minimal moon logo on deep navy (#0A1628) background, geometric white crescent moon shape, 2-3 tiny star dots nearby in soft blue (#4A90D9) and lavender (#B8A9C9), flat clean design, no gradients, no shadows, no cartoon face, no cute elements, modern brand mark style, square format, centered with generous padding",
        "first_tweets": [
            "i slept terribly for years. 5.5 hours of broken sleep. tried melatonin, CBD, weighted blankets, white noise. nothing stuck. then i made 4 changes. 3 weeks later: 7.5 hours of deep sleep. here's the protocol.",
            "the 4 changes that fixed my sleep: 1) 8pm screen cutoff (or orange glasses). 2) 65F bedroom temp. 3) 10pm lights out, same time every night. 4) morning sunlight within 30 min of waking. that's it. no supplements.",
            "your room is probably 72F. sleep research says 60-67F is optimal. your body needs to drop 2-3 degrees core temp to initiate sleep. a warm room fights this. turn down the thermostat tonight.",
        ],
        "accounts_to_follow": [
            "@hubaborermanlab - neuroscience of sleep",
            "@drmaboratthewwalker - Why We Sleep author",
            "@risaborescience - circadian rhythm research",
            "@eightsleep - sleep tech (study their content style)",
            "@sleepaborefoundation - evidence-based sleep tips",
        ],
    },
    {
        "filename": "05_MEMES_entertainment.md",
        "handle": "@printmaxx_memes",
        "display_name": "printmaxx memes",
        "email": "printmaxxer@protonmail.com",
        "niche": "Memes / Entertainment / Engagement Farming",
        "proxy": "Decodo-1",
        "gologin_profile": "Profile-Meta",
        "brand_colors": "Black background, white text, no branding",
        "bio": "memes about building stuff on the internet. solopreneur humor. if you get it, you get it.",
        "pfp_prompt": "Simple white skull emoji icon on pure black background, flat design, no gradients, clean vector style, centered, minimalist, slightly cartoonish but not childish, square format",
        "first_tweets": [
            "me: i'll just build one more script before bed\n\n3 hours later: i now have a cron system that monitors 16 jobs, auto-resumes crashes, and generates a morning TODO\n\nthe script i originally needed: still not written",
            "solopreneur stages:\n\n1. i'll build one app\n2. actually i'll build 7 apps\n3. and 10 digital products\n4. and 3 newsletters\n5. and cold email\n6. i have built everything and sold nothing\n7. the bottleneck is me logging into websites",
            "\"how's the startup going?\"\n\n80 python scripts. 7 apps. 1,661 leads. 1,278 posts. 10 products.\n\nrevenue: $0\n\n\"so... not great?\"\n\ni just need to log into vercel",
        ],
        "accounts_to_follow": [
            "@shaboritposting - tech memes",
            "@staborartupjokes - startup humor",
            "@devaborhumor - developer memes",
            "@inabordiehackers - indie hacker community",
            "@pipelineabuser - aggressive solopreneur energy",
        ],
    },
]


def generate_quick_sheet(account: dict) -> str:
    """Generate a single account cheat sheet as markdown."""
    tweets_text = ""
    for i, tweet in enumerate(account["first_tweets"], 1):
        tweets_text += f"### Tweet {i}\n\n```\n{tweet}\n```\n\n"

    follows_text = ""
    for follow in account["accounts_to_follow"]:
        follows_text += f"- {follow}\n"

    sheet = f"""# Twitter Quick Sheet: {account['display_name']}

Niche: {account['niche']}
Open this on your phone during signup. Copy-paste everything.

---

## 1. Signup info

| Field | Value |
|-------|-------|
| URL | https://twitter.com/signup |
| Email | `{account['email']}` |
| Handle | `{account['handle']}` |
| Display Name | `{account['display_name']}` |
| GoLogin Profile | {account['gologin_profile']} |
| Proxy | {account['proxy']} |

---

## 2. Bio (copy-paste this)

```
{account['bio']}
```

---

## 3. Profile pic prompt (paste into Leonardo.ai or Gemini)

Brand colors: {account['brand_colors']}

```
{account['pfp_prompt']}
```

---

## 4. First 3 tweets (post these after creation)

{tweets_text}
---

## 5. First 5 accounts to follow

{follows_text}
---

## 6. Post-creation settings

- [ ] Dark mode ON
- [ ] Notifications: DMs and mentions only (turn off likes/retweets)
- [ ] Privacy: Keep account public
- [ ] Verify email address
- [ ] Like 3 posts in your niche before tweeting
- [ ] Follow the 5 accounts above
- [ ] Wait 24 hours before posting (or at minimum, engage for 1 hour first)

---

## 7. After creation, run this command

```bash
python3 scripts/account_tracker.py add --platform twitter --username "{account['handle'].lstrip('@')}" --email "{account['email']}" --status CREATED
```
"""
    return sheet


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    created_files = []
    for account in ACCOUNTS:
        content = generate_quick_sheet(account)
        filepath = OUTPUT_DIR / account["filename"]
        filepath.write_text(content)
        created_files.append(str(filepath))
        print(f"Created: {filepath.name}")

    # Generate index file
    index_content = """# Twitter Account Quick Sheets

Open these one at a time on your phone during account creation.
Each file has everything you need: email, handle, bio, profile pic prompt, first tweets, who to follow.

## Files

| # | Account | Niche | File |
|---|---------|-------|------|
"""
    for i, account in enumerate(ACCOUNTS, 1):
        index_content += f"| {i} | {account['handle']} | {account['niche']} | [{account['filename']}]({account['filename']}) |\n"

    index_content += """
## Order of creation

1. PRINTMAXXER (hub account, everything links back here)
2. DailyAnchor (faith, Ramadan tracker cross-promo)
3. 3-Hour Physique (fitness)
4. SleepMaxx (sleep/wellness)
5. printmaxx_memes (entertainment, engagement farming)

## Time estimate

~5 min per account = ~25 min total for all 5 Twitter accounts.

## After all accounts are created

```bash
# Check account status
python3 scripts/account_tracker.py status

# Start warmup tracking
python3 scripts/account_tracker.py warmup
```
"""
    index_path = OUTPUT_DIR / "INDEX.md"
    index_path.write_text(index_content)
    print(f"Created: {index_path.name}")

    print(f"\nDone. {len(created_files)} quick sheets + 1 index at {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
