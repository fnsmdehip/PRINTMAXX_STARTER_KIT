# ColdMaxx — Screenshot Capture Spec

## Required Dimensions
- **iOS:** 1290 x 2796px (iPhone 15 Pro Max)
- **Android:** 1080 x 1920px minimum

## Screenshot List

### Screenshot 1: Framework Selector
**Screen:** Main tab bar
**State:**
- 3 tabs visible: AIDA | PAS | BAB
- "AIDA" tab selected (indigo highlight)
- Form beneath with fields:
  - Your company: "Acme Agency"
  - Prospect company: "TechStartup Inc"
  - What you do: "B2B cold email campaigns"
  - Key benefit: "10x reply rates"
**Caption:** "3 proven frameworks. Pick one."

### Screenshot 2: Generated Email — AIDA
**Screen:** Email output card
**State:**
- AIDA card fully rendered showing:
  - Subject line: "Quick question about TechStartup's outreach"
  - Email body (full AIDA structure)
  - Word count: 87 words
  - Read time: 25 sec
  - Copy button visible
- Card style: dark card with indigo AIDA label badge
**Caption:** "Generated in seconds"

### Screenshot 3: All 3 Variants Side by Side
**Screen:** Results with all 3 framework cards stacked
**State:**
- AIDA card (indigo badge)
- PAS card (green badge)
- BAB card (cyan badge)
- Each showing preview of first 2 lines
- "Copy" button on each
**Caption:** "3 angles. Pick the one that converts."

### Screenshot 4: Subject Line Generator
**Screen:** Subject lines tab
**State:**
- 5 subject line options listed
- "Quick question about [company]" — Curiosity style
- "How [competitors] are 10x-ing replies" — Competitor style
- "2 min read: [outcome]" — Time style
- "Honest question for [name]" — Direct style
- "Saw [company] on LinkedIn…" — Research style
- Each with a style label and copy button
**Caption:** "5 subject lines per campaign"

### Screenshot 5: Spam Checker
**Screen:** Spam score tab
**State:**
- Spam score gauge showing 92/100 "Excellent"
- Green checkmarks for: Word count, No spam triggers, No caps abuse, No excessive punctuation
- 1 warning: "Consider personalizing first line"
**Caption:** "Built-in spam score check"

### Screenshot 6: Follow-Up Sequence
**Screen:** Follow-up tab
**State:**
- Day 1: Initial email (collapsed preview)
- Day 4: Follow-up 1 — "Checking in" (preview)
- Day 10: Follow-up 2 — "Last reach out" (preview)
- Day 21: Breakup email
**Caption:** "Auto-generate 4-touch sequences"

## Capture Method
```bash
# Playwright automated:
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 430, "height": 932})
    page.goto("https://coldmaxx.surge.sh")
    # Fill form fields first, then screenshot
    page.fill("[name='company']", "TechStartup Inc")
    page.click("button[data-framework='aida']")
    page.screenshot(path="coldmaxx_01_framework.png")
```

## File Naming
```
coldmaxx_ios_01_framework_selector.png
coldmaxx_ios_02_aida_email.png
coldmaxx_ios_03_all_variants.png
coldmaxx_ios_04_subject_lines.png
coldmaxx_ios_05_spam_checker.png
coldmaxx_ios_06_followup_sequence.png
```
