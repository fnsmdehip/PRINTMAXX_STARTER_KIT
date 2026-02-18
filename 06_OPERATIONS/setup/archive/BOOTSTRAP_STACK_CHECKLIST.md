# Bootstrap Stack Checklist

**What to tell Claude when done, what automates immediately, what needs human.**

---

## HOW TO USE THIS FILE

1. Open each URL and create account
2. When done, tell Claude exactly what's in the "Tell Claude" column
3. Claude runs immediate automations
4. Human handles items marked HUMAN REQUIRED
5. Move to next priority

---

## PRIORITY 1: BLOCKING INFRASTRUCTURE

These block ALL other work. Do first.

| Service | URL | Tell Claude When Done | Claude Automates | Human Required |
|---------|-----|----------------------|------------------|----------------|
| **Apple Developer** | https://developer.apple.com/programs/enroll/ | "apple dev done, team ID: [ID]" | Updates app.json configs, prepares certificates | Payment ($99), D-U-N-S if business |
| **Google Play** | https://play.google.com/console/signup | "play console done" | Updates android configs, prepares keystore | Payment ($25) |
| **Cloudflare** | https://cloudflare.com | "cloudflare done, email: [email]" | Sets up DNS templates, CDN rules | Add domains manually |
| **Porkbun** | https://porkbun.com | "porkbun done" | Nothing yet (need domain) | Buy domains when ready |

**After Priority 1 complete, tell Claude:** "infra done, ready for domains"

---

## PRIORITY 2: HOSTING + DEPLOYMENT

| Service | URL | Tell Claude When Done | Claude Automates | Human Required |
|---------|-----|----------------------|------------------|----------------|
| **Vercel** | https://vercel.com | "vercel done, connected to github" | Deploys landing site, sets up preview URLs | Connect GitHub OAuth |
| **Oracle Cloud** | https://oracle.com/cloud/free | "oracle done, region: [region]" | Creates VPS setup scripts, configures firewall rules | Credit card for verification (not charged) |
| **Hetzner** | https://hetzner.com | "hetzner done" | Prepares server provisioning scripts | Add payment when ready to spin up |

**After Priority 2 complete, tell Claude:** "hosting ready"

---

## PRIORITY 3: LEAD DATA + OUTREACH

| Service | URL | Tell Claude When Done | Claude Automates | Human Required |
|---------|-----|----------------------|------------------|----------------|
| **Apollo.io** | https://apollo.io | "apollo done" | Creates saved searches, exports lead lists to LEDGER/leads.csv | Connect LinkedIn for enrichment |
| **Hunter.io** | https://hunter.io | "hunter done, API key: [key]" | Adds to email verification workflow | None |
| **Instantly** | https://instantly.ai | "instantly done, API key: [key]" | Sets up warmup campaigns, imports sequences from EMAIL_SEQUENCES.md | Add sending domains, buy inboxes |
| **Smartlead** | https://smartlead.ai | "smartlead done" | Alternative to Instantly, same automations | Add sending domains |

**After Priority 3 complete, tell Claude:** "outreach stack ready"

---

## PRIORITY 4: SOCIAL SCHEDULING

| Service | URL | Tell Claude When Done | Claude Automates | Human Required |
|---------|-----|----------------------|------------------|----------------|
| **Buffer** | https://buffer.com | "buffer done, connected: [platforms]" | Schedules posts from NICHE_ACCOUNT_CONTENT_CALENDAR.md | Connect social accounts |
| **Hypefury** | https://hypefury.com | "hypefury done, X connected" | Schedules X threads, auto-retweets | Connect X account |
| **TweetHunter** | https://tweethunter.io | "tweethunter done" | Creates engagement campaigns, tweet scheduling | Connect X account |

**After Priority 4 complete, tell Claude:** "social scheduling ready"

---

## PRIORITY 5: AI CONTENT TOOLS

| Service | URL | Tell Claude When Done | Claude Automates | Human Required |
|---------|-----|----------------------|------------------|----------------|
| **Leonardo.ai** | https://leonardo.ai | "leonardo done" | Generates app icons, marketing assets | None |
| **ElevenLabs** | https://elevenlabs.io | "elevenlabs done, API key: [key]" | Generates voiceovers for videos via MCP | None |
| **Kling** | https://klingai.com | "kling done" | Generates AI video clips | None |
| **HeyGen** | https://heygen.com | "heygen done" | Creates AI avatar videos | Payment for beyond trial |
| **Canva** | https://canva.com | "canva done" | Creates social templates | None |
| **CapCut** | https://capcut.com | "capcut done" | Nothing (manual editing tool) | None |

**After Priority 5 complete, tell Claude:** "content tools ready"

---

## PRIORITY 6: PROXIES + VERIFICATION

| Service | URL | Tell Claude When Done | Claude Automates | Human Required |
|---------|-----|----------------------|------------------|----------------|
| **Soax** | https://soax.com | "soax done, API: [credentials]" | Configures proxy rotation for automation scripts | Payment, choose proxy type |
| **Smartproxy** | https://smartproxy.com | "smartproxy done" | Alternative proxy config | Payment |
| **SMSPool** | https://smspool.net | "smspool done, balance: $[X]" | Uses for account verification automation | Add balance |

**After Priority 6 complete, tell Claude:** "proxies ready for automation"

---

## PRIORITY 7: LINKEDIN AUTOMATION

| Service | URL | Tell Claude When Done | Claude Automates | Human Required |
|---------|-----|----------------------|------------------|----------------|
| **Expandi** | https://expandi.io | "expandi done, linkedin connected" | Imports sequences from LINKEDIN_TEMPLATES.md, starts campaigns | Connect LinkedIn, set daily limits |
| **Dripify** | https://dripify.io | "dripify done" | Alternative to Expandi | Connect LinkedIn |
| **Waalaxy** | https://waalaxy.com | "waalaxy done" | Free tier LinkedIn automation | Connect LinkedIn |

**After Priority 7 complete, tell Claude:** "linkedin automation ready"

---

## PRIORITY 8: NEWSLETTER + CRM

| Service | URL | Tell Claude When Done | Claude Automates | Human Required |
|---------|-----|----------------------|------------------|----------------|
| **Beehiiv** | https://beehiiv.com | "beehiiv done, publication: [name]" | Creates welcome sequence, imports subscriber from LEDGER/leads.csv | Design templates |
| **Substack** | https://substack.com | "substack done" | Nothing (manual platform) | Write posts |
| **HubSpot** | https://hubspot.com/crm | "hubspot done" | Syncs leads from LEDGER, creates deal pipeline | None |
| **Notion** | https://notion.so | "notion done" | Creates project templates | None |

---

## PRIORITY 9: PAID ENGAGEMENT (OPTIONAL)

| Service | URL | Tell Claude When Done | Claude Automates | Human Required |
|---------|-----|----------------------|------------------|----------------|
| **MediaMister** | https://mediamister.com | "mediamister done" | Nothing (manual orders) | Place orders per ALGO_SAFE_PROTOCOL |
| **Growthoid** | https://growthoid.com | "growthoid done" | Nothing (managed service) | Payment, provide account access |
| **Kicksta** | https://kicksta.co | "kicksta done" | Nothing (managed service) | Connect IG, set targets |

---

## PRIORITY 10: AGED ACCOUNTS (OPTIONAL)

| Service | URL | Tell Claude When Done | Claude Automates | Human Required |
|---------|-----|----------------------|------------------|----------------|
| **AccsMarket** | https://accsmarket.com | "bought [platform] account, login: [user]" | Adds to ACCOUNTS.csv, creates warmup schedule | Purchase, change password, add 2FA |
| **Fameswap** | https://fameswap.com | "bought IG account: [handle]" | Adds to tracking, creates warmup schedule | Verify account, escrow |
| **SocialTradia** | https://socialtradia.com | "bought account" | Tracking | Verify, transfer |

---

## WHAT CLAUDE CAN AUTOMATE IMMEDIATELY

Once you have accounts, Claude can run these without human:

### Content Generation
- Generate 50+ social posts from NICHE_ACCOUNT_CONTENT_CALENDAR.md
- Create app icons with Leonardo/Gemini
- Generate voiceovers with ElevenLabs MCP
- Build Remotion marketing videos

### Lead Generation
- Export Apollo leads matching ICP to LEDGER/leads.csv
- Verify emails via Hunter
- Score and segment leads

### Email Outreach
- Import sequences to Instantly/Smartlead
- Set up warmup campaigns
- Schedule sends (after warmup complete)

### Social Scheduling
- Queue posts to Buffer/Hypefury
- Schedule X threads
- Create engagement campaigns

### Research
- Run /daily-research for alpha discovery
- Update ALPHA_STAGING.csv
- Monitor HIGH_SIGNAL_SOURCES.csv accounts

### Ralph Loops (Overnight)
- comprehensive_research loop
- content_social loop
- alpha_hunter loop
- All 13 loops via `./ralph/run_all_loops.sh`

---

## WHAT NEEDS HUMAN IN LOOP

These ALWAYS require human:

### Payments
- Developer account fees
- Domain purchases
- Subscription upgrades
- Proxy/SMS top-ups
- Engagement service orders

### Account Security
- Password changes on purchased accounts
- 2FA setup
- OAuth connections
- API key generation (some platforms)

### Platform Connections
- LinkedIn OAuth
- X/Twitter OAuth
- Instagram login
- Social account linking

### Publishing
- App Store submissions (review required)
- First email sends (verify deliverability)
- Public social posts (brand review)
- Newsletter sends

### Verification
- Phone verification (manual sometimes)
- Identity verification
- Business verification
- Domain ownership verification

---

## WHAT COMES NEXT

### After Bootstrap Complete:

**Week 1: Warmup Phase**
1. Email inboxes warming (Instantly handles automatically)
2. Social accounts aging (light manual activity)
3. LinkedIn connection building (Expandi slow start)
4. Domain reputation building

**Week 2: Content Phase**
1. Generate 100+ social posts
2. Create 10 Remotion videos
3. Build app marketing assets
4. Write 5 email sequences

**Week 3: Outreach Phase**
1. Start cold email campaigns
2. Begin LinkedIn outreach
3. Launch social posting schedule
4. Run first paid engagement

**Week 4: Scale Phase**
1. Double email volume
2. Add more sending domains
3. A/B test content
4. Track FUNNEL_METRICS.csv

---

## QUICK START COMMAND

Tell Claude this to begin:

```
"opening bootstrap URLs now, will report back as each is done"
```

Then for each service:
```
"[service] done, [any required info like API key or ID]"
```

Claude will track progress and automate what's possible.

---

## TRACKING PROGRESS

Claude maintains progress in:
- `LEDGER/ACCOUNTS.csv` - All account credentials (encrypted)
- `LEDGER/FUNNEL_METRICS.csv` - Performance tracking
- `.ralph/progress.md` - Automation status

---

## EMERGENCY CONTACTS

If account gets banned/suspended:
1. Document in OPS/logs/BANNED_[platform].md
2. Check warmup protocols in ULTIMATE_ACCOUNT_WARMUP_GUIDE.md
3. Review limits in EDGE_GROWTH_TACTICS.md
4. Consider aged account purchase

---

**Last Updated:** 2026-01-26
