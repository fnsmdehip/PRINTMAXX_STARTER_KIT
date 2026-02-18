# 3-Hour Physique - Lead magnet

## Lead magnet name

The 4-Week Starter Program: Build Strength at Home in 3 Hours a Week

---

## What they get

A PDF with:

1. Complete 4-week workout plan
   - 3 workouts per week
   - 45 minutes each
   - Minimal equipment (pull-up bar, resistance bands, or nothing)

2. Exercise library with descriptions and photos
   - 12 exercises total
   - Easier and harder variations for each

3. Weekly progression guidelines
   - When to add reps
   - When to make exercises harder
   - How to know if you're doing it right

4. Equipment alternatives
   - What to use if you don't have a pull-up bar
   - How to add resistance without weights
   - The backpack trick for progressive overload

Format: PDF, printable, includes workout log pages.

---

## Landing page copy

### Headline

Build strength at home in 3 hours a week

### Subheadline

A free 4-week program for busy people. No gym. Minimal equipment.

### Body

You don't need a gym membership to get stronger.

You don't need 2 hours a day.

You need 3 hours per week and a system that actually works.

This 4-week starter program is the foundation of the 3-Hour Physique. It's free because I want you to see results before you spend anything.

**What's inside:**

- Complete 4-week workout plan
- 12 exercises with photos and instructions
- Progressions for each week
- Equipment alternatives (or no equipment at all)

**What's not inside:**

- Complicated periodization
- Equipment you don't have
- 90-minute workout days

3 workouts. 45 minutes each. 4 weeks. See what happens.

### CTA

**[Get the free program]**

Enter your email. Check your inbox. Start today.

---

## Delivery mechanism

1. User enters email on landing page
2. ConvertKit automation triggers
3. Immediate email with PDF download link
4. Email sequence starts 24 hours later (see EMAIL_SEQUENCE.md)

### Tech setup

- Landing page: Next.js page at /magnet/4-week-starter
- Form: ConvertKit embedded form
- Automation: ConvertKit sequence with 24-hour delay
- PDF hosting: Gumroad (unlisted) or Cloudflare R2

### Follow-up sequence

After delivery, subscriber enters the 7-email nurture sequence for 3-Hour Physique. First email sends 24 hours after download.
