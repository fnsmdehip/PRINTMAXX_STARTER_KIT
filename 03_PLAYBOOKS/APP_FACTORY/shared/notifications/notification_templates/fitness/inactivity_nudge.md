# Inactivity nudge notifications

Fitness apps: WalkToUnlock, FemFit

Sent when user hasn't moved or opened the app by midday.

---

## Primary variants

**Variant A - Gentle**
- Title: "Quick stretch?"
- Body: "Even 5 minutes counts."

**Variant B - Progress check**
- Title: "[X]% done"
- Body: "You're [Y] steps from halfway."

**Variant C - Low pressure**
- Title: "Still time"
- Body: "Half the day left to hit your goal."

---

## Midday check-in

**At 25% of goal**
- Title: "Getting there"
- Body: "[X] more steps to halfway."

**At 50% of goal**
- Title: "Halfway"
- Body: "You're on track. Keep going."

**At 0% of goal by noon**
- Title: "Start small"
- Body: "A 10-minute walk gets you 1,000 steps."

---

## WalkToUnlock specific

**Variant A**
- Title: "Phone still locked"
- Body: "Quick walk to unlock your apps."

**Variant B**
- Title: "[X] steps left"
- Body: "Short walk unlocks your phone."

---

## FemFit specific

**Variant A**
- Title: "Haven't started?"
- Body: "Today's workout is only [X] minutes."

**Variant B**
- Title: "5 minute option"
- Body: "Too busy for full workout? Do the short version."

---

## Timing and frequency

- First nudge: 12 PM (if < 25% of goal)
- Second nudge: 4 PM (if < 50% of goal)
- No more than 2 inactivity nudges per day
- Skip if user explicitly marked "rest day"
- Reduce frequency if user ignores 3 in a row

---

## Smart scheduling

- If user typically active 3-5 PM, skip noon nudge
- If user completed goal early yesterday, be gentler today
- During weekends, shift timing 2 hours later

---

## Anti-annoyance

1. Max 2 nudges per day
2. If ignored 5 days in a row, switch to weekly digest
3. Never send during work hours if user has "work mode" enabled
4. Stop nudges after 6 PM
