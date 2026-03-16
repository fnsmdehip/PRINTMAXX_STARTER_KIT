# PrayerLock — Google Play Listing

## App Name (50 chars max)
PrayerLock: Prayer Habit Tracker

## Short Description (80 chars max)
Prayer timer, streak tracker, Qibla compass & tasbih counter. Free, offline.

## Full Description (4000 chars max)

**Build a prayer habit that sticks. Timer, streak, Qibla compass, and tasbih — in one private, offline app.**

PrayerLock gives you everything you need to maintain a consistent prayer habit. No account. No ads. Works offline. Your data stays on your device.

**PRAYER TIMER**
Set focused prayer sessions from 5 to 60 minutes. Circular countdown with gentle completion sound. Optional ambient sounds to eliminate distractions.

**STREAK TRACKER**
Track prayer consistency across the full year — one square per day, GitHub-style. Milestones at 7, 14, 30, 60, and 90 days. Seeing the streak keeps you praying.

**QIBLA COMPASS**
Find the direction of Mecca from anywhere in the world. Accurate GPS + compass bearing. Works offline after location is set.

**TASBIH COUNTER**
Digital prayer bead counter with vibration feedback. Targets at 33, 99, or custom. Session history saved automatically.

**DAILY VERSE**
One Quranic or Biblical verse per day. Share with one tap.

---

**WHY PRAYERLOCK**

✓ No account required
✓ Completely offline — works without internet
✓ Private — nothing leaves your device
✓ Interfaith — designed for Muslims and Christians
✓ Free, no paywalls on core features
✓ No ads

---

**FOR MUSLIMS:** Qibla compass, tasbih with dhikr targets (33/99), Islamic geometric design, Arabic verse display

**FOR CHRISTIANS:** Daily Bible verse, prayer streak, quiet time tracker

---

Build your habit. Keep your streak.

## Category
Lifestyle

## Content Rating
Everyone

## Price
Free

## Privacy Policy URL
https://prayerlock.surge.sh/privacy-policy.html

## Feature Graphic (1024x500px)
Dark navy background with Islamic geometric pattern, PrayerLock in teal, crescent moon graphic, streak fire emoji, tagline "Build your prayer habit"

## Screenshots (1080x1920px)
1. Prayer timer (circular countdown active)
2. Streak tracker (30-day streak visible)
3. Qibla compass (needle pointing toward Mecca)
4. Tasbih counter (33/99 targets)
5. Daily verse (Arabic + English)
6. Home screen overview

## Permissions Required
- `ACCESS_FINE_LOCATION` — for Qibla direction calculation
- `VIBRATE` — tasbih haptic feedback

## Submission Method (TWA)
```bash
# 1. Ensure deployed at HTTPS
npx surge . prayerlock.surge.sh

# 2. Convert icon to PNG
inkscape icon-1024.svg -o icon-1024.png -w 1024 -h 1024
# Also create icon-512.png, icon-192.png

# 3. Update manifest.json — replace SVG data URI icons with PNG files

# 4. Init TWA
npx @bubblewrap/cli init --manifest https://prayerlock.surge.sh/manifest.json

# 5. Build
bubblewrap build

# 6. Sign + upload to Play Console
```

## TWA Checklist
- [ ] Icons converted to PNG (manifest.json updated)
- [ ] assetlinks.json at /.well-known/assetlinks.json
- [ ] Location permission declared in manifest
- [ ] Play Console account created ($25)
- [ ] App screenshots captured on actual Android device

## Market Notes
- Muslim prayer apps: Muslim Pro has 100M+ downloads. Market is proven and enormous.
- Key differentiator: privacy-first, no account, no data collection — directly opposite Muslim Pro's data scandal (2020 controversy)
- Target keyword: "Muslim prayer app" + "prayer tracker"
- Consider Arabic store listing separately for MENA market
