# DeskBreak — Product Requirements Document

**Date:** 2026-03-17
**Status:** BUILDING
**Target deploy:** deskbreak.surge.sh

## Problem
Remote workers and developers spend 8-12 hours at a desk daily. Most forget to:
- Rest their eyes (causes digital eye strain — 60M people affected)
- Check posture (back pain = #1 work-related injury)
- Drink water (67% are mildly dehydrated at work)
- Move (sitting >6h/day = 40% increased mortality risk)

Existing apps: FocusMate, Stretchly are clunky desktop apps. No polished PWA.

## Solution
**DeskBreak** — a beautiful PWA that runs 4 automated timers in the browser:
- 👁 Eye Break: Every 20 min → 20-second 20-ft lookaway (20-20-20 rule)
- 🧍 Posture Check: Every 30 min → 30-second posture correction
- 💧 Hydration: Every 60 min → drink 1 glass of water
- 🤸 Movement: Every 90 min → 2-min stretch/walk

## Target User
Developers, remote workers, solopreneurs, students. Ages 22-40. Already uses productivity apps.

## Monetization
1. **Free tier**: All 4 timers, basic streak tracking
2. **DeskBreak Pro** ($2.99/mo): Custom intervals, analytics, keyboard shortcuts, themes
3. **Affiliate revenue**: "Upgrade Your Setup" section — Amazon links for:
   - Ergonomic chair (avg $8 commission)
   - Standing desk converter ($15 commission)
   - Blue light glasses ($3 commission)
   - Quality water bottle ($2 commission)

## Success Metrics
- 500 installs in 30 days
- 20% streak >3 days (engagement signal)
- 2% affiliate click-through
- Email capture: 5% of users opt-in for "Perfect Desk Setup" PDF

## Tech
- Pure HTML/CSS/JS PWA (no build step, deploys to surge.sh in 30 seconds)
- localStorage for streak/settings
- Web Notifications API for break alerts
- Service Worker for offline capability
- Web Audio API for gentle break sound

## ASO Keywords
Primary: desk break reminder, pomodoro desk wellness, eye strain timer, 20 20 20 rule app
Secondary: posture reminder app, hydration reminder, desk break timer, remote work wellness
Long-tail: free desk break reminder pwa, eye break 20 20 20 timer app, remote worker health app
