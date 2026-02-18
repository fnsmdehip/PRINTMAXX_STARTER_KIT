# Daily Anchor System - Lead magnet

## Lead magnet name

The Morning Verse Guide: 14 Scriptures to Start Your Day Grounded

---

## What they get

A simple PDF with:

1. 14 morning verses organized by what you need:
   - When you need peace (4 verses)
   - When you need direction (4 verses)
   - When you need strength (3 verses)
   - When you need gratitude (3 verses)

2. How to use a verse in the morning (not a study, just absorption)

3. The "speak it" technique (why saying it out loud changes things)

4. One-week challenge: use one verse per day, track how you feel

Format: PDF, printable, 4 pages, no fluff.

---

## Landing page copy

### Headline

14 verses to start your morning grounded

### Subheadline

A simple guide to using Scripture before your phone. Free PDF.

### Body

Your morning sets your day.

If it starts with stress, scrolling, and rushing, that energy carries through.

If it starts with truth, the day feels different.

This guide gives you 14 verses organized by what you need. Peace when you're anxious. Direction when you're uncertain. Strength when you're tired.

The goal isn't a long study. It's one verse, absorbed before the noise starts.

**What's inside:**

- 14 verses organized by need
- How to actually use a verse (not just read it)
- The "speak it" technique
- One-week challenge to try it

**What's not inside:**

- Lengthy devotionals
- Guilt about your quiet time
- Suggestions to wake up at 5am

4 pages. Takes 5 minutes to read. Try one verse tomorrow morning.

### CTA

**[Get the free guide]**

Enter your email. Check your inbox. Start tomorrow.

---

## Delivery mechanism

1. User enters email on landing page
2. ConvertKit automation triggers
3. Immediate email with PDF download link
4. Email sequence starts 24 hours later (see EMAIL_SEQUENCE.md)

### Tech setup

- Landing page: Next.js page at /magnet/morning-verse-guide
- Form: ConvertKit embedded form
- Automation: ConvertKit sequence with 24-hour delay
- PDF hosting: Gumroad (unlisted) or Cloudflare R2

### Follow-up sequence

After delivery, subscriber enters the 7-email nurture sequence for Daily Anchor System. First email sends 24 hours after download.
