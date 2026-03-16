# Enterprise Automation Solutions — Full Rebuild Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild enterpriseautomation.solutions as a productized automation service, fully integrated into the PRINTMAXX venture ecosystem with legal framework, subcontractor system, and automated lead pipeline.

**Architecture:** Multi-page static website (7 HTML files) deployed to surge.sh. Legal documents stored in PRODUCTS/EAS/. PRINTMAXX integration via venture_autonomy.py registration, ops bridge cache entries, CLAUDE.md/SOUL.md/memory updates, and cron wiring.

**Tech Stack:** HTML/CSS/JS (vanilla, no frameworks), Python (automation scripts), n8n/Bland AI/Cal.com (service delivery stack), surge.sh (deployment)

---

## File Structure

```
MONEY_METHODS/EAS/                          # EAS venture root
├── website/                                # Website source files
│   ├── index.html                          # Homepage
│   ├── packages.html                       # Productized packages
│   ├── results.html                        # Case studies / results
│   ├── playbooks.html                      # Free resources + lead capture
│   ├── calculator.html                     # Interactive ROI calculator
│   ├── contact.html                        # Smart intake form
│   └── book.html                           # Cal.com scheduling embed
├── legal/                                  # Legal document templates
│   ├── MSA_TEMPLATE.md                     # Master Services Agreement
│   ├── SOW_TEMPLATE.md                     # Statement of Work template
│   ├── RISK_DISCLOSURE.md                  # AI risk disclosure addendum
│   └── SUBCONTRACTOR_AGREEMENT.md          # Independent contractor agreement
├── playbooks/                              # Subcontractor delivery playbooks
│   ├── SIGNAL_MAP_PLAYBOOK.md              # Signal Map ($1,500) delivery steps
│   ├── PHONE_PILOT_PLAYBOOK.md             # Phone Pilot ($3,500) delivery steps
│   ├── OPS_PILOT_PLAYBOOK.md               # Ops Pilot ($4,500) delivery steps
│   └── MANAGED_OPS_PLAYBOOK.md             # Managed Ops (monthly) delivery steps
├── outreach/                               # EAS-specific outreach templates
│   ├── cold_email_sequences.md             # Cold email sequences for EAS
│   └── lead_scoring_config.json            # EAS-specific lead scoring weights
└── EAS_VENTURE_README.md                   # Venture overview for system agents

AUTOMATIONS/eas_lead_pipeline.py            # EAS lead generation pipeline script
```

**Files to modify:**
- `.claude/CLAUDE.md` — Add EAS venture reference + auto-load instructions
- `AUTOMATIONS/SOUL.md` — Add EAS behavioral directive
- `OPS/PERSISTENT_TASK_TRACKER.md` — Add EAS venture tasks
- `OPS/PRINTMAXX_SYSTEM_MAP.md` — Add EAS to system map
- Memory: `.claude/projects/-Users-macbookpro/memory/` — Add EAS memory file

---

## Chunk 1: Website — Homepage + Shared Styles

### Task 1: Build the homepage (index.html)

**Files:**
- Create: `MONEY_METHODS/EAS/website/index.html`

The homepage is the largest file and establishes the shared CSS/design system used by all pages. "Private Bank" aesthetic: black bg, gold accents, serif headings, subtle scroll animations.

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p MONEY_METHODS/EAS/website MONEY_METHODS/EAS/legal MONEY_METHODS/EAS/playbooks MONEY_METHODS/EAS/outreach
```

- [ ] **Step 2: Write index.html**

Single-file HTML page containing:
- Shared `<style>` block with full CSS design system (reused via copy for other pages)
- Nav: EAS logo (text) | Packages | Results | Playbooks | Calculator | Contact | [Book a Call] button
- Hero section: Serif headline "Your phones answered. Your meetings actioned. Your back office quiet." + subtitle + 2 CTAs (Book a Pilot, See Packages) + 3 stat cards (90-day payback, 10-day pilots, 0 vendor lock-in)
- Trust bar: "Built on tools you already use" — Zoom, HubSpot, Slack, Zapier, Make, n8n logos (text-only, no images)
- Value props grid: 4 cards (Outcomes not tools, Open-source option, Transparent pricing, Managed with SLAs)
- Services overview: 3 cards (Phone, Meetings, Ops) with bullet features
- Slack digest mockup section: Example daily digest with real-looking data
- Process: 4-step (Signal map → Pilot build → Prove ROI → Scale & govern) with numbered steps
- FAQ: 4 accordion items
- Final CTA: "Ready to stop losing money to manual processes?" + 2 buttons
- Footer: copyright, privacy, contact, book links

Design specs:
- Background: #0a0a0a
- Gold accent: #c9a227
- Cream text: #f5f0e8
- Muted text: #888
- Card bg: rgba(201, 162, 39, 0.05) with 1px border rgba(201, 162, 39, 0.15)
- Headings: Georgia, serif
- Body: -apple-system, system-ui, sans-serif
- Max-width: 1200px centered
- Scroll animations: IntersectionObserver fade-in-up (elements start opacity:0, translateY:30px → animate to visible)
- Stat numbers: count-up animation when scrolled into view
- Cards: subtle lift on hover (translateY -2px, shadow increase)
- Mobile: fully responsive, hamburger nav, sticky CTA
- No em dashes anywhere in copy
- All copy in PRINTMAXXER voice (lowercase energy, specific numbers, consequence-first)

- [ ] **Step 3: Verify in browser**

Open locally or deploy to surge.sh and verify:
- Dark background renders correctly
- Gold accents visible but not overwhelming
- Serif headings distinct from sans-serif body
- Scroll animations trigger on scroll (not on load)
- Mobile responsive (test at 375px width)
- No em dashes in any copy
- No AI vocabulary (leverage, delve, comprehensive, etc.)

- [ ] **Step 4: Deploy to verify**

```bash
surge MONEY_METHODS/EAS/website eas-preview.surge.sh
```

---

### Task 2: Build the packages page (packages.html)

**Files:**
- Create: `MONEY_METHODS/EAS/website/packages.html`

- [ ] **Step 1: Write packages.html**

4 pricing tiers in 2x2 grid:
1. **Signal Map** — $1,500 flat, 5 days. Workflow audit, ROI model, pilot architecture, executive readout.
2. **Phone Pilot** — $3,500 flat, 10 days. AI phone concierge, CRM logging, escalation logic, 30-day monitoring. Badge: "Most booked"
3. **Ops Pilot** — $4,500 flat, 10 days. One back-office automation (n8n/Make/Zapier), rollback, runbook, training.
4. **Managed Ops** — $1,500-$3,000/mo. Monitoring, monthly iteration, incident response, ROI reporting.

Each card: tier label, price, description, 4 bullet deliverables, CTA button.
Below cards: "What's included in every engagement" section (consultant, telemetry, security review, training).
Billing section: 50% to reserve, 50% on launch. Managed bills monthly.
FAQ section: 4 questions specific to pricing.
Final CTA: ROI calculator link + booking link.

- [ ] **Step 2: Verify pricing matches spec and renders correctly**

---

### Task 3: Build results page (results.html)

**Files:**
- Create: `MONEY_METHODS/EAS/website/results.html`

- [ ] **Step 1: Write results.html**

3 case studies (use realistic but clearly marked as illustrative until real clients exist):
1. Multi-location dental group — AI phone concierge. 48% fewer missed calls, 1.8 FTE saved, $37k recall revenue.
2. HVAC/plumbing company — ops automation. 19% more booked jobs, zero missed parts orders, tech NPS 7.1→8.6.
3. Marketing agency — meeting intelligence. 12 hrs/week leadership time saved, 35% action completion increase.

Each: industry tag, company name (placeholder), headline result, Situation/Solution/Outcomes format.
2 testimonial blockquotes with name + role.
CTA: "Want to see dashboards and SOPs?"

- [ ] **Step 2: Verify renders correctly**

---

### Task 4: Build playbooks page (playbooks.html)

**Files:**
- Create: `MONEY_METHODS/EAS/website/playbooks.html`

- [ ] **Step 1: Write playbooks.html**

3 playbook cards:
1. "AI receptionist in a weekend" — Ops + RevOps audience
2. "Meetings to actions" — Leadership + project teams
3. "Stack picker: Zapier vs Make vs n8n" — IT + automation leads

Each: audience tag, title, description, "What you get" section, email capture to access.
Workshop CTA section at bottom.

Key: playbook access requires email (lead magnet). Form posts to a simple endpoint or mailto.

- [ ] **Step 2: Verify renders correctly**

---

### Task 5: Build ROI calculator page (calculator.html)

**Files:**
- Create: `MONEY_METHODS/EAS/website/calculator.html`

- [ ] **Step 1: Write calculator.html**

Interactive calculator with sliders/inputs:
- Team size (1-50, default 5)
- Average hourly rate ($30-$200, default $72)
- Hours wasted on manual tasks per week (1-40, default 10)

Real-time calculation:
- Monthly value recovered = team_size × hourly_rate × hours_wasted × 4.33
- Annual savings = monthly × 12
- Recommended pilot tier (auto-suggest based on savings)
- ROI timeline (payback in X days)

Display as animated numbers with gold highlights.
Below calculator: CTA to book a pilot with pre-filled data.

All calculation runs client-side (JavaScript). No backend needed.

- [ ] **Step 2: Test calculations are correct**

Manual verification:
- 5 people × $72/hr × 10 hrs × 4.33 = $15,588/month
- Annual: $186,660
- Should recommend "Ops Pilot" tier

- [ ] **Step 3: Verify renders correctly**

---

### Task 6: Build contact page (contact.html)

**Files:**
- Create: `MONEY_METHODS/EAS/website/contact.html`

- [ ] **Step 1: Write contact.html**

Smart intake form with:
- Name*, Work email*, Company, Website, Phone, Industry
- Textarea: "What do you want to automate?"
- Heuristics checkboxes (keep from current site — they're good for lead qualification):
  - Website tech lag
  - No online booking/chat
  - Phone-first business
  - Industry fit
  - Reviews mid-range
  - Stale marketing content
  - Contact friction
- Submit button: "Send introduction"

Below form: "What happens next?" + "Need NDAs?" + "Prefer email?" sections.

Form action: mailto:hello@enterpriseautomationsolutions.com (until proper backend).

- [ ] **Step 2: Verify form renders and submits correctly**

---

### Task 7: Build booking page (book.html)

**Files:**
- Create: `MONEY_METHODS/EAS/website/book.html`

- [ ] **Step 1: Write book.html**

Simple page with:
- Heading: "Book a working session"
- Subtext: "15 minutes. We'll review your workflows, identify quick wins, and scope a pilot if there's fit."
- Cal.com embed placeholder (iframe with data-cal-link attribute, loads when Cal.com is set up)
- Fallback: email link if Cal.com not yet configured
- 3 info cards below: "What to prepare", "What we'll cover", "What happens after"

- [ ] **Step 2: Verify renders correctly**

---

### Task 8: Deploy full website

- [ ] **Step 1: Deploy all pages to surge.sh**

```bash
surge MONEY_METHODS/EAS/website enterpriseautomation-preview.surge.sh
```

Note: This deploys a preview. Final deployment to enterpriseautomation.solutions requires DNS update.

- [ ] **Step 2: Test all page links work**

Navigate to each page from the nav. Verify no broken links.

- [ ] **Step 3: Test mobile responsiveness**

Check each page at 375px, 768px, 1024px, 1440px widths.

---

## Chunk 2: Legal & Business Documents

### Task 9: Write Master Services Agreement

**Files:**
- Create: `MONEY_METHODS/EAS/legal/MSA_TEMPLATE.md`

- [ ] **Step 1: Write MSA**

Sections:
1. Parties (EAS = "Company", Client = "Client")
2. Services (reference SOW for specifics)
3. Fees and Payment (50% upfront, 50% on delivery; managed = monthly arrears)
4. Term and Termination (30-day notice for managed; project = until completion)
5. Intellectual Property (client owns deliverables; EAS retains methodology/playbooks/tools)
6. Confidentiality (mutual NDA built-in)
7. Limitation of Liability (CAPPED at fees paid in prior 12 months; no consequential damages)
8. Indemnification (mutual; client indemnifies for their data/compliance; EAS indemnifies for gross negligence)
9. Warranties and Disclaimers (reasonable care; NO warranty of error-free; AI systems may produce incorrect outputs)
10. Data Protection (data handling per DPA if applicable; HIPAA BAA available on request)
11. Dispute Resolution (binding arbitration, Wyoming jurisdiction)
12. Force Majeure (AI model changes, API deprecation, third-party service failures)
13. Entire Agreement, Amendments, Severability
14. Signature block

Key liability protections:
- Explicit "as-is" disclaimer for AI outputs
- Capped liability at fees paid
- No consequential/punitive damages
- Client responsible for their own regulatory compliance
- Force majeure covers AI model deprecation

- [ ] **Step 2: Review for completeness against design spec**

---

### Task 10: Write SOW Template

**Files:**
- Create: `MONEY_METHODS/EAS/legal/SOW_TEMPLATE.md`

- [ ] **Step 1: Write SOW**

Fill-in-the-blank template with:
- Project name, client name, dates
- Package selected (Signal Map / Phone Pilot / Ops Pilot / Managed)
- Scope of work (specific deliverables per package)
- Out of scope (explicitly listed)
- Timeline with milestones
- Acceptance criteria
- Fees and payment schedule
- Change order process (scope changes = new SOW, additional fees)
- Key contacts

- [ ] **Step 2: Verify template is complete**

---

### Task 11: Write Risk Disclosure Addendum

**Files:**
- Create: `MONEY_METHODS/EAS/legal/RISK_DISCLOSURE.md`

- [ ] **Step 1: Write disclosure**

Client acknowledges:
1. AI phone systems may be detected as AI by some callers
2. Automation workflows may produce errors requiring human review
3. AI-generated summaries may miss context or misinterpret intent
4. Third-party APIs and services may change, degrade, or discontinue
5. Automations require ongoing monitoring and maintenance
6. EAS is not liable for business decisions made based on automated outputs
7. Client is responsible for compliance with industry regulations (HIPAA, GDPR, CCPA, etc.)
8. Performance metrics are estimates based on similar implementations, not guarantees
9. Data processed by automations passes through third-party services (listed per project)
10. Client retains full control and can disable any automation at any time

Tiered risk disclosure:
- Standard risk (most projects): items 1-10 above
- Elevated risk (financial/healthcare data): additional data handling provisions
- High risk (regulated industries): requires separate compliance review

- [ ] **Step 2: Review for legal completeness**

---

### Task 12: Write Subcontractor Agreement

**Files:**
- Create: `MONEY_METHODS/EAS/legal/SUBCONTRACTOR_AGREEMENT.md`

- [ ] **Step 1: Write agreement**

Sections:
1. Relationship (independent contractor, NOT employee; 1099)
2. Services (reference playbook for deliverables)
3. Compensation (milestone-based: 30% start, 40% draft, 30% client acceptance)
4. Non-Disclosure (client info, pricing, methodology, playbooks — 3 years)
5. Non-Compete (cannot directly solicit EAS clients — 12 months post-termination; geographically and scope-limited for enforceability)
6. Non-Solicitation (cannot solicit EAS employees/contractors — 24 months)
7. IP Assignment (all work product → EAS/client; contractor retains pre-existing tools)
8. Quality Standards (must follow playbook; remediation process for defects)
9. Termination (either party, 14 days notice; immediate for breach)
10. Insurance (contractor maintains own insurance)
11. Dispute Resolution (binding arbitration)

Key protections:
- Narrow non-compete (only direct client solicitation, not "can't do automation consulting")
- Courts throw out overly broad non-competes; narrow = enforceable
- Milestone payments = leverage if quality is bad
- IP assignment = contractor can't resell what they built for your clients

- [ ] **Step 2: Review for enforceability concerns**

---

## Chunk 3: Subcontractor Playbooks

### Task 13: Write Signal Map delivery playbook

**Files:**
- Create: `MONEY_METHODS/EAS/playbooks/SIGNAL_MAP_PLAYBOOK.md`

- [ ] **Step 1: Write playbook**

Step-by-step delivery manual for the $1,500 Signal Map package:

Day 1-2: Discovery
- Schedule 60-min kickoff call with client
- Document current tools, workflows, team structure
- Access to observe 1 day of operations (shadow or screen share)
- Capture: call volume, meeting load, manual touchpoints, error rates

Day 3-4: Analysis
- Map all workflows in visual diagram (use draw.io or Miro template)
- Score each workflow: automation potential (1-10), ROI impact (1-10), complexity (1-10)
- Build ROI model: hours saved × hourly rate × 12 months
- Identify top 3 automation candidates ranked by ROI / complexity ratio

Day 5: Deliverables
- Executive readout document (5-10 pages):
  - Current state map
  - Top 3 automation opportunities with ROI projections
  - Recommended pilot scope
  - Architecture diagram for pilot
  - Tool recommendations (vendor-neutral)
  - Timeline and investment for pilot phase
- 30-minute presentation to stakeholders

Quality checkpoints:
- Checkpoint 1 (Day 2): Workflow maps complete. Sub submits for review.
- Checkpoint 2 (Day 4): ROI model complete. Sub submits for review.
- Checkpoint 3 (Day 5): Final deliverable. Sub submits for review before client presentation.

- [ ] **Step 2: Verify playbook is detailed enough for a new subcontractor to follow**

---

### Task 14: Write Phone Pilot delivery playbook

**Files:**
- Create: `MONEY_METHODS/EAS/playbooks/PHONE_PILOT_PLAYBOOK.md`

- [ ] **Step 1: Write playbook**

10-day delivery for AI phone concierge ($3,500):

Day 1-2: Setup
- Client provides: business phone number, call routing rules, CRM access, escalation contacts
- Set up Bland AI account (100 free calls/day)
- Configure voice personality, greeting, and business context
- Write initial call scripts (greeting, routing, FAQ, appointment booking, escalation)

Day 3-5: Build
- Connect Bland AI to client CRM (HubSpot/Salesforce) via n8n/Make
- Build escalation tree: which calls transfer to human, which get handled by AI
- Set up call logging: every call → CRM contact note with transcript summary
- Configure after-hours behavior (voicemail → SMS notification, follow-up email)
- Build SMS notification pipeline for escalated calls

Day 6-7: Test
- Run 20 test calls covering all scenarios
- QA rubric: greeting correct, routing correct, CRM logging correct, escalation works
- Fix issues found in testing
- Document edge cases and fallback behavior

Day 8-9: Launch
- Go live on subset of calls (50% routing to AI, 50% to human)
- Monitor first 24 hours closely
- Adjust scripts based on real call patterns
- Provide training to client team (30-min session)

Day 10: Handoff
- Deliver runbook with all configurations documented
- Set up 30-day monitoring dashboard (call volume, resolution rate, escalation rate)
- Deliver telemetry access to client
- Schedule 2-week check-in call

Quality checkpoints: 3 review gates (Day 2, Day 7, Day 10).

- [ ] **Step 2: Verify playbook completeness**

---

### Task 15: Write Ops Pilot and Managed Ops playbooks

**Files:**
- Create: `MONEY_METHODS/EAS/playbooks/OPS_PILOT_PLAYBOOK.md`
- Create: `MONEY_METHODS/EAS/playbooks/MANAGED_OPS_PLAYBOOK.md`

- [ ] **Step 1: Write Ops Pilot playbook**

10-day delivery for one back-office automation ($4,500). Similar structure to Phone Pilot but for n8n/Make/Zapier workflow builds. Covers: requirements gathering, workflow design, build, test, rollback plan, runbook, training.

- [ ] **Step 2: Write Managed Ops playbook**

Monthly recurring delivery ($1,500-3,000/mo). Covers: monitoring setup, incident response SLA, monthly velocity roadmap, usage/ROI reporting, backlog grooming, iteration cycles.

- [ ] **Step 3: Verify both playbooks**

---

## Chunk 4: PRINTMAXX System Integration

### Task 16: Register EAS as a PRINTMAXX venture

**Files:**
- Create: `MONEY_METHODS/EAS/EAS_VENTURE_README.md`
- Modify: `OPS/PRINTMAXX_SYSTEM_MAP.md`
- Modify: `OPS/PERSISTENT_TASK_TRACKER.md`

- [ ] **Step 1: Write EAS venture README**

Overview document that any PRINTMAXX agent can read to understand the EAS venture:
- What it is (productized automation service)
- Revenue model (packages + managed ops)
- Lead pipeline (PRINTMAXX scrapers → EAS outreach → close → subcontractor delivery)
- Key files and paths
- Current status
- Blockers

- [ ] **Step 2: Update system map**

Add EAS venture to the STRUCTURE TREE and agent sections of `OPS/PRINTMAXX_SYSTEM_MAP.md`.

- [ ] **Step 3: Update persistent task tracker**

Add EAS venture section with:
- Website deployment status
- Legal docs status
- Lead pipeline status
- Human blockers (DBA filing, bank account, Cal.com setup)

- [ ] **Step 4: Verify updates**

---

### Task 17: Update CLAUDE.md with EAS venture instructions

**Files:**
- Modify: `.claude/CLAUDE.md`

- [ ] **Step 1: Add EAS reference to KEY FILE LOCATIONS table**

Add row: `EAS venture | MONEY_METHODS/EAS/ (website, legal, playbooks, outreach)`

- [ ] **Step 2: Add EAS to venture commands in Technical Quick Reference**

Add EAS lead pipeline command to the commands list.

- [ ] **Step 3: Add instruction for auto-loading EAS context on new venture creation**

Add to CLAUDE.md a rule: "When creating any new venture/op, ensure it is registered in: PRINTMAXX_SYSTEM_MAP.md, PERSISTENT_TASK_TRACKER.md, CLAUDE.md key files table, SOUL.md directives, and memory system. This is automatic, not manual."

- [ ] **Step 4: Verify changes don't break existing CLAUDE.md structure**

Read the file and check for formatting issues.

---

### Task 18: Update SOUL.md with EAS behavioral directives

**Files:**
- Modify: `AUTOMATIONS/SOUL.md`

- [ ] **Step 1: Add EAS directive**

After the existing kill/double-down triggers, add:
- EAS venture kill trigger: <3 qualified leads per month after 60 days → reassess positioning
- EAS venture double-down trigger: >2 pilots closed per month → invest in paid ads, hire dedicated sales sub
- EAS behavioral: all agents must treat EAS client data with confidentiality; never expose client details in content, alpha entries, or cross-venture outputs

- [ ] **Step 2: Verify SOUL.md remains under 120 lines (keep it lean)**

---

### Task 19: Add EAS memory entry

**Files:**
- Create: `.claude/projects/-Users-macbookpro/memory/eas_venture.md`
- Modify: `.claude/projects/-Users-macbookpro/memory/MEMORY.md`

- [ ] **Step 1: Write memory file**

```markdown
---
name: EAS Venture
description: Enterprise Automation Solutions — productized automation service under DBA, integrated as PRINTMAXX venture
type: project
---

Enterprise Automation Solutions (EAS) is a productized automation service business.
- Domain: enterpriseautomation.solutions
- DBA under existing Wyoming LLC
- Packages: Signal Map ($1,500), Phone Pilot ($3,500), Ops Pilot ($4,500), Managed Ops ($1,500-3,000/mo)
- Delivery: subcontractors following playbooks
- Lead gen: PRINTMAXX scrapers repurposed (savvy_lead_scraper, nationwide_scraper, mass_outreach)
- Design: "Private Bank" aesthetic (black/gold/serif)
- Files: MONEY_METHODS/EAS/ (website, legal, playbooks, outreach)
- Status: Building (Mar 2026)

**Why:** Service revenue diversifies PRINTMAXX beyond digital products/apps. Higher margins than product sales. Recurring revenue via Managed Ops.
**How to apply:** When agents process local biz leads or outbound opportunities, also score for EAS fit. Cross-pollinate EAS leads with local biz website service (S02).
```

- [ ] **Step 2: Add pointer to MEMORY.md**

Add line: `- [eas_venture.md](eas_venture.md) — Enterprise Automation Solutions venture (productized service, website, legal, subcontractor system)`

---

### Task 20: Build EAS lead pipeline script

**Files:**
- Create: `AUTOMATIONS/eas_lead_pipeline.py`

- [ ] **Step 1: Write the pipeline script**

Python script that:
1. Reads scored leads from `AUTOMATIONS/leads/` (output of savvy_lead_scraper)
2. Filters for EAS-fit leads using EAS-specific criteria:
   - Website quality score < 40 (needs help)
   - Has phone number (phone-first business)
   - Industry in target list (dental, legal, HVAC, plumbing, agency)
   - Reviews > 20 (established business, can afford services)
3. Generates personalized outreach email per lead using cold email template
4. Outputs to `MONEY_METHODS/EAS/outreach/eas_leads_ready.csv` (Instantly.ai compatible)
5. Logs pipeline stats

CLI: `python3 AUTOMATIONS/eas_lead_pipeline.py --generate`

- [ ] **Step 2: Write EAS cold email sequences**

Create `MONEY_METHODS/EAS/outreach/cold_email_sequences.md` with 3-email sequence:
- Email 1: "Your [specific issue] is costing you $X/month" (value-first, specific to their website analysis)
- Email 2: Case study relevant to their industry
- Email 3: "Last note" with ROI calculator link

- [ ] **Step 3: Write EAS lead scoring config**

Create `MONEY_METHODS/EAS/outreach/lead_scoring_config.json` with weights:
- website_quality_inverse: 30% (worse site = better lead)
- phone_first: 20% (phone-heavy business = needs phone automation)
- industry_fit: 20% (target industries score higher)
- review_count: 15% (established = can pay)
- location_tier: 15% (higher population = bigger operation)

- [ ] **Step 4: Test pipeline runs without errors**

```bash
python3 AUTOMATIONS/eas_lead_pipeline.py --generate 2>&1 | head -20
```

---

### Task 21: Add EAS to cron schedule

**Files:**
- Modify: crontab

- [ ] **Step 1: Add cron entries**

```
# === EAS VENTURE PIPELINE ===
0 8 * * 1-5 cd $BASE && $PYTHON AUTOMATIONS/eas_lead_pipeline.py --generate >> AUTOMATIONS/logs/eas_pipeline.log 2>&1
# === END EAS VENTURE PIPELINE ===
```

- [ ] **Step 2: Verify cron entry added**

```bash
crontab -l | grep eas
```

---

### Task 22: Add new venture creation auto-registration rule to CLAUDE.md

**Files:**
- Modify: `.claude/CLAUDE.md`

- [ ] **Step 1: Add rule to CORE RULES section**

Add as Rule 15 or append to Rule 7:

```
### 15. NEW VENTURE AUTO-REGISTRATION (MANDATORY)

When creating ANY new venture, op, or business line, AUTOMATICALLY update ALL of these:

1. `OPS/PRINTMAXX_SYSTEM_MAP.md` — Add to STRUCTURE TREE + relevant sections
2. `OPS/PERSISTENT_TASK_TRACKER.md` — Add venture section with status + blockers
3. `.claude/CLAUDE.md` — Add to KEY FILE LOCATIONS table
4. `AUTOMATIONS/SOUL.md` — Add kill/double-down triggers for the venture
5. `.claude/projects/-Users-macbookpro/memory/` — Create memory file + update MEMORY.md
6. `CONTENT/social/posting_queue/` — Generate launch content (Rule 9: Max Squeeze)

This is NOT optional. Skipping any step = orphan venture that agents can't see.
Every session automatically loads these files, so new ventures are visible to all agents from the next session onward.
```

- [ ] **Step 2: Verify rule doesn't duplicate existing rules**

---

## Chunk 5: Final Integration & Deploy

### Task 23: Full deploy and smoke test

- [ ] **Step 1: Deploy website to surge.sh**

```bash
surge MONEY_METHODS/EAS/website eas-preview.surge.sh
```

- [ ] **Step 2: Test all 7 pages load**

Navigate to each page URL and verify rendering.

- [ ] **Step 3: Test ROI calculator**

Input test values and verify calculations match expected output.

- [ ] **Step 4: Test contact form**

Submit test form and verify mailto link works.

- [ ] **Step 5: Run EAS lead pipeline**

```bash
python3 AUTOMATIONS/eas_lead_pipeline.py --generate
```

Verify output CSV is created and contains leads.

- [ ] **Step 6: Verify all system files updated**

Check: CLAUDE.md, SOUL.md, PRINTMAXX_SYSTEM_MAP.md, PERSISTENT_TASK_TRACKER.md, memory files.

- [ ] **Step 7: Generate launch content (Rule 9)**

Create 4 tweets + 1 thread about EAS launch in `CONTENT/social/posting_queue/eas_launch.txt`.

- [ ] **Step 8: Update OPS/DEPLOYMENT_URLS.md**

Add all EAS URLs to the deployment tracker.

- [ ] **Step 9: Final status update**

Update PERSISTENT_TASK_TRACKER.md with completed status.
