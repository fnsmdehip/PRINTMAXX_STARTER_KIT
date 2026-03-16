# InvoiceForge — Screenshot Capture Spec

## Required Dimensions
- **iOS (App Store):** 1290 x 2796px (iPhone 15 Pro Max — 6.7")
- **Android (Play Store):** 1080 x 1920px minimum

## Screenshot List (5 required, 8 max for App Store)

### Screenshot 1: Invoice Creation
**Screen:** Main invoice form
**State to show:**
- Client name filled in: "Mike's Plumbing LLC"
- Template selected: Plumbing
- Business name: "John Smith Plumbing"
- At least 3 line items (Service call $150, Labor 2hrs $200, Parts $85)
- Tax set to 10%
- Total showing: $467.50
**Caption overlay (optional):** "Build invoices in under 60 seconds"

### Screenshot 2: Line Items & Auto-Calc
**Screen:** Line items section
**State:**
- 4 line items with descriptions, qty, rate, total columns
- Subtotal bar showing
- Tax row showing
- Grand total highlighted in emerald green
**Caption:** "Auto-calculates everything"

### Screenshot 3: PDF Preview
**Screen:** Print/PDF preview dialog (browser native)
**State:**
- Show the invoice rendered as it would look in a PDF
- Logo area, business info, client info, line items, total, payment button
**Caption:** "Export professional PDFs instantly"

### Screenshot 4: Invoice History
**Screen:** Saved invoices list
**State:**
- 4-5 invoices listed with status badges
  - INV-001: PAID (green badge) — $467.50
  - INV-002: PENDING (yellow badge) — $1,200.00
  - INV-003: OVERDUE (red badge) — $340.00
  - INV-004: DRAFT (gray badge) — $89.00
**Caption:** "Track paid, pending & overdue"

### Screenshot 5: Trade Templates
**Screen:** Template selector
**State:**
- Grid of templates visible: Plumbing, Electrical, HVAC, Contractor, Landscaping, Cleaning, Freelance
- Each with icon and name
- "Plumbing" highlighted/selected
**Caption:** "Built-in trade templates"

## Capture Methods

### Method A: Playwright (automated, recommended)
```python
# From project root:
python3 AUTOMATIONS/playwright_site_tester.py --url https://invoiceforge.surge.sh --screenshot

# Or write a custom capture script:
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 430, "height": 932})
    page.goto("https://invoiceforge.surge.sh")
    page.wait_for_load_state("networkidle")
    page.screenshot(path="screenshot_1_invoice_form.png", full_page=False)
    browser.close()
```

### Method B: Manual in Browser
1. Open https://invoiceforge.surge.sh in Chrome
2. Open DevTools → Toggle device toolbar (Cmd+Shift+M)
3. Set to "iPhone 15 Pro Max" (393x852 logical, 3x DPR = 1179x2556)
4. Fill in the invoice fields per spec above
5. Use Cmd+Shift+3 or browser screenshot extension
6. Upload to App Store Connect / Play Console

### Method C: iPhone screenshot (highest quality)
1. Add app to home screen on iPhone
2. Open app, fill in fields per spec
3. Press side button + volume up for screenshot
4. Crop to remove status bar if needed

## Pro Tip: Screenshot Frame Tool
Use Mockuphone.com or Shots.so to add a device frame around the raw screenshot before uploading to App Store (higher conversion rate with frames showing).

## File Naming Convention
```
invoiceforge_ios_01_invoice_form.png
invoiceforge_ios_02_line_items.png
invoiceforge_ios_03_pdf_preview.png
invoiceforge_ios_04_history.png
invoiceforge_ios_05_templates.png

invoiceforge_android_01_invoice_form.png
... (same screens, different resolution)
```
