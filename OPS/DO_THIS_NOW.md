# DO THIS NOW
Day 58. $0 revenue. 136 sites deployed. 13 products built. 1,588 posts queued. 54 cold emails drafted.
No comparison tables. No research. Just do these steps.

---

## STEP 1: Fix surge login (5 min)
Open Terminal on your Mac:
```
cd /Users/macbookpro/Documents/p/PRINTMAXX_STARTER_KITttttt
npx surge logout
npx surge login
```
When it asks for email: type `printmaxxweb@gmail.com`
When it asks for password: type your password
Done. Close terminal.

---

## STEP 2: Gumroad account (15 min)
1. Open Chrome
2. Go to `gumroad.com`
3. Click "Start selling"
4. Sign up with your email
5. Verify email (check inbox, click link)
6. Go to Settings > Payments > Connect Stripe (you already have Stripe)
7. Click "New Product"
8. Upload this file from your Mac: `GUMROAD_INSTANT_UPLOAD/03_vibe_coding_playbook.pdf`
9. Title: `Vibe Coding Playbook`
10. Price: `$47`
11. Click Publish
12. Repeat for the other 12 products:

| Title | Price | File |
|-------|-------|------|
| 5 AI Prompts (free lead magnet) | $0 | `10_free_lead_magnet.pdf` |
| Funnel Teardown Guide | $7 | `09_funnel_teardown_guide.pdf` |
| Sleep YouTube Starter Kit | $17 | `08_sleep_youtube_starter.pdf` |
| Solopreneur Tech Stack | $17 | `07_solopreneur_tech_stack.pdf` |
| 50 Viral Tweet Templates | $19 | `12_viral_tweet_templates.pdf` |
| Cold Email Playbook | $27 | `05_cold_email_playbook.pdf` |
| Twitter/X Growth Playbook | $27 | `06_twitter_growth_playbook.pdf` |
| 73 Cold Email Subject Lines | $29 | `11_cold_email_subject_lines.pdf` |
| Local Biz Cold Email Pack | $39 | `13_local_biz_cold_email_pack.pdf` |
| AI Content Farm Blueprint | $47 | `04_ai_content_farm_blueprint.pdf` |
| Vibe Coding Playbook | $47 | `03_vibe_coding_playbook.pdf` |
| AI Automation Toolkit | $47 | `02_ai_automation_toolkit.pdf` |
| Claude Code Agent Bible | $47 | `14_CLAUDE_CODE_AGENT_BIBLE.pdf` |

All files are in: `DIGITAL_PRODUCTS/ready_to_sell/pdfs/`

---

## STEP 3: Fiverr account (20 min)
1. Go to `fiverr.com`
2. Click "Join"
3. Sign up with email
4. Click "Become a Seller"
5. Fill out profile: name, photo, bio "AI automation expert"
6. Click "Create a Gig"
7. Title: "I will build you a custom AI automation system"
8. Category: Programming & Tech > AI Services
9. Packages: $100 basic / $300 standard / $500 premium
10. Write description (or copy from `MONEY_METHODS/FREELANCE/fiverr_gigs/`)
11. Publish
12. Make 4 more gigs same way

---

## STEP 4: Affiliate signups (30 min)
Open these 5 tabs one at a time. Sign up for each. Save the affiliate link they give you.

1. `semrush.com/partners` -- sign up -- save link
2. `convertkit.com/affiliates` -- sign up -- save link
3. `beehiiv.com/referrals` -- sign up -- save link
4. `instantly.ai/affiliates` -- sign up -- save link
5. `smartlead.ai/affiliate` -- sign up -- save link

Then open Terminal:
```
python3 AUTOMATIONS/payment_integrator.py --replace-placeholders
```

---

## STEP 5: Tailscale -- control Mac from phone (5 min)
On your Mac, open Terminal:
```
/opt/homebrew/bin/tailscale login
```
Browser opens. Sign in with Google or GitHub.
Write down the IP it shows (looks like `100.64.0.1`).

On your iPhone:
1. App Store > search "Tailscale" > install
2. Open Tailscale > sign in with SAME account you just used
3. Open Safari > type `http://YOUR_IP:9999` (use the IP from above)
4. You see the PRINTMAXX dashboard
5. Tap the share button > "Add to Home Screen" > name it "PRINTMAXX"

---

## STEP 6: RustDesk -- see Mac screen on phone (2 min)
On your Mac:
1. Press Cmd+Space > type "RustDesk" > open it (it's in ~/Applications/)
2. If Mac asks for Screen Recording permission > click Allow
3. If Mac asks for Accessibility permission > click Allow
4. See the ID number on screen (like `123 456 789`) -- write it down
5. Click the gear icon > Security > set a permanent password

On your iPhone:
1. App Store > search "RustDesk" > install
2. Open RustDesk > type the ID number from step 4
3. Type your password
4. You now see your Mac screen. Tap to click. Type to type.

---

## STEP 7: Twitter @PRINTMAXXER (10 min)
1. Open Chrome > go to `x.com` > log in as @PRINTMAXXER
2. Click your profile pic > Edit Profile
3. Click the header image area > upload `MEDIA/generated_images/twitter_banner.png`
4. Click the profile pic circle > upload `MEDIA/generated_images/twitter_pfp.png`
5. Bio: open `CONTENT/social/TWITTER_PROFILE_SPEC.md` on your Mac > copy the bio text > paste
6. Click Save
7. Click the compose button (feather icon)
8. Open any file in `CONTENT/social/posting_queue/` > copy a tweet > paste > Post

---

## STEP 8: GoLogin for multi-account (10 min)
1. Open Chrome > go to `gologin.com/pricing`
2. Click "Professional" ($24/mo for 100 profiles)
3. Sign up and pay
4. Download the Mac app from their dashboard
5. Install it, open it, sign in
6. To manage from phone: use RustDesk (step 6) to see the GoLogin app on your Mac

---

## STEP 9: Cheap email domain (15 min)
1. Go to `namecheap.com`
2. Search for a domain (like `yourname-mail.com`) -- find one under $10/yr
3. Buy it
4. Go to `purelymail.com` > sign up ($10/yr -- not per month, per YEAR)
5. Click "Add Domain"
6. Type your new domain
7. They show you DNS records to add -- go back to Namecheap > DNS settings > add them
8. Wait 5 min for DNS
9. Create email addresses: `acct1@yourdomain.com`, `acct2@yourdomain.com`, etc.

---

## THAT'S IT. YOU'RE DONE.

Time: ~2 hours total
Cost: ~$85 first month

What's now live:
- 13 products on Gumroad (people can buy them)
- 5 gigs on Fiverr (clients can hire you)
- 5 affiliate programs (your pages earn commission)
- Dashboard on your iPhone (monitor everything)
- Mac screen on your iPhone (control everything)
- Twitter active (content flowing)
- GoLogin ready (create more accounts)
- Email domain (unique emails for each account)

Next step: open `OPS/COMPLETE_SOCIAL_INFRA_STACK.md` and follow the "SPEED SETUP" to create social accounts in GoLogin profiles with proxies.
