# Wappalyzer Workflow — Tech Stack Intelligence for Cold Outbound

## Why This Matters

Wappalyzer tells you what software a website is running. That means you can:
- Identify companies using Competitor A → pitch them on switching to a better tool (or your service)
- Find companies with a gap in their stack → pitch filling that gap
- Build "technographic" lead lists: "all companies using Webflow but not using HubSpot"
- Sell to the exact person responsible for the tool you detected (VP Marketing owns HubSpot)

This is how you go from spray-and-pray cold email to surgical, hyper-relevant outreach.

---

## Tool Options

### Free Options
| Tool | Method | Limits |
|------|--------|--------|
| Wappalyzer Chrome Extension | Manual, one site at a time | Unlimited, but slow |
| builtwith.com | Single site lookup | 1 lookup/day on free |
| whatruns.com | Chrome extension | Manual only |
| `python-whois` + header detection | Manual scraping | DIY, no API cost |

### Paid Options (Best ROI)
| Tool | Price | Credits/Lookups | Best For |
|------|-------|----------------|----------|
| Wappalyzer API | Free tier: 50/mo, Starter $29/mo: 2,000/mo | Per domain lookup | Batch enrichment |
| Wappalyzer Business | $249/mo | Unlimited API + lead lists | Scale (100K+ leads) |
| BuiltWith | $295/mo | Unlimited | Pre-built tech lists (buy tech users directly) |
| Apollo.io | $49/mo (Basic) | 10K exports | Has technographics built-in for common tools |
| Clay | $149/mo | 10K credits | Waterfall enrichment incl. tech stack |

**Best value:** Apollo Basic at $49/mo includes Salesforce/HubSpot/Shopify/Stripe detection for most B2B companies. Use Wappalyzer API for the edge cases Apollo misses.

---

## Technographic Triggers by Service Offering

### If you sell cold email setup / outbound infrastructure:

**Target:** Companies using HubSpot or Salesforce CRM but NOT using Instantly/Lemlist/Outreach/Salesloft

```
Pitch angle: "you have the CRM but no outbound engine. you're leaving pipeline on the table."
Stack detected: HubSpot + missing outbound tool
Conversion signal: they're already paying for CRM = serious about sales, budget exists
```

**How to find them:**
1. BuiltWith: Technology Lists → HubSpot → filter by company size 10-200 employees
2. Export CSV of 10,000 HubSpot-using companies
3. Cross-reference: remove any that also show Outreach/SalesLoft/Lemlist in their stack
4. Remaining list = perfect target for your cold email setup service

### If you sell Webflow/website builds:

**Target:** Companies using WordPress + Elementor or aging HTML sites

```
Pitch angle: "your site is built on [detected stack]. it's holding back your conversions."
Stack detected: WordPress 5.x + Elementor + WP Plugins (site feels bloated)
Conversion signal: they're already spending money on site infrastructure
```

### If you sell SEO services:

**Target:** Companies using Shopify or WooCommerce with no SEO tool

```
Stack detected: Shopify + missing Yoast/SEMrush/Clearscope/SurferSEO integrations
Pitch angle: "your store has zero on-page SEO setup. these 3 changes would get you traffic."
```

### If you sell ChatGPT/AI chatbot installs:

**Target:** Companies using Intercom or Zendesk but not using AI layer on top

```
Stack detected: Intercom (older plan without AI) or plain Zendesk
Pitch angle: "you're paying $74/mo for Intercom. I can add AI that handles 60% of tickets automatically."
```

### If you sell email marketing (Klaviyo setup):

**Target:** Shopify/WooCommerce stores without Klaviyo

```
Stack detected: Shopify + no Klaviyo + no Mailchimp flows
Pitch angle: "you have [X] SKUs on Shopify and zero email automation. most ecom stores get 30% of revenue from email."
```

---

## Batch Detection Workflow (Python + Wappalyzer API)

```python
#!/usr/bin/env python3
"""
Batch tech stack detection for cold outbound lead lists.
Input: CSV with 'domain' column
Output: CSV with tech_stack and pitch_angle columns added
"""

import requests
import csv
import time
import os
from typing import Optional

WAPPALYZER_API_KEY = os.environ.get('WAPPALYZER_API_KEY', '')

# Service-to-stack-gap mapping
PITCH_ANGLES = {
    'cold_email_setup': {
        'has': ['HubSpot', 'Salesforce'],
        'missing': ['Instantly', 'Lemlist', 'Outreach', 'Salesloft', 'Apollo'],
        'pitch': 'Has CRM but no cold outbound tool — pitch outbound infrastructure setup'
    },
    'webflow_rebuild': {
        'has': ['WordPress', 'Elementor'],
        'missing': ['Webflow'],
        'pitch': 'Running WordPress + Elementor — pitch modern Webflow rebuild for performance + CRO'
    },
    'shopify_email': {
        'has': ['Shopify'],
        'missing': ['Klaviyo', 'Mailchimp', 'Omnisend'],
        'pitch': 'Shopify store with no email automation — pitch Klaviyo setup + flow build'
    },
    'ai_chatbot': {
        'has': ['Intercom', 'Zendesk'],
        'missing': ['ChatGPT', 'Tidio AI', 'Crisp'],
        'pitch': 'Has live chat but no AI layer — pitch chatbot install + training'
    },
    'seo_audit': {
        'has': ['Shopify', 'WooCommerce', 'WordPress'],
        'missing': ['Yoast SEO', 'SEMrush', 'Ahrefs', 'SurferSEO'],
        'pitch': 'Has content site but no SEO tool connected — pitch technical SEO audit'
    }
}

def get_tech_stack(domain: str) -> Optional[list]:
    """Fetch tech stack from Wappalyzer API."""
    clean = domain.replace('https://', '').replace('http://', '').rstrip('/')
    url = f"https://api.wappalyzer.com/v2/lookup/?urls=https://{clean}"
    headers = {"x-api-key": WAPPALYZER_API_KEY}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data:
                return [t['name'] for t in data[0].get('technologies', [])]
    except Exception as e:
        print(f"Error for {domain}: {e}")
    return []

def detect_pitch_angle(tech_stack: list) -> str:
    """Match tech stack to highest-value pitch angle."""
    angles = []
    for service, rules in PITCH_ANGLES.items():
        has_required = any(t in tech_stack for t in rules['has'])
        missing_required = not any(t in tech_stack for t in rules['missing'])
        if has_required and missing_required:
            angles.append(rules['pitch'])
    return ' | '.join(angles) if angles else 'generic_pitch'

def process_leads(input_file: str, output_file: str):
    with open(input_file, 'r') as f_in:
        reader = csv.DictReader(f_in)
        rows = list(reader)
        fields = reader.fieldnames + ['tech_stack', 'pitch_angle', 'wappalyzer_done']

    results = []
    for i, row in enumerate(rows):
        domain = row.get('domain') or row.get('website', '')
        if not domain:
            row.update({'tech_stack': '', 'pitch_angle': 'no_domain', 'wappalyzer_done': 'false'})
            results.append(row)
            continue

        print(f"[{i+1}/{len(rows)}] Checking {domain}...")
        stack = get_tech_stack(domain)
        pitch = detect_pitch_angle(stack)

        row['tech_stack'] = ', '.join(stack)
        row['pitch_angle'] = pitch
        row['wappalyzer_done'] = 'true'
        results.append(row)

        time.sleep(0.6)  # Stay under 100 req/min on Starter plan

    with open(output_file, 'w', newline='') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)

    print(f"Done. {len(results)} leads enriched → {output_file}")

if __name__ == '__main__':
    process_leads(
        'AUTOMATIONS/leads/crunchbase_raw_latest.csv',
        'AUTOMATIONS/leads/leads_with_stack.csv'
    )
```

---

## Apollo.io Alternative (No Wappalyzer Needed)

Apollo.io Basic ($49/mo) includes technographic filters for the most common B2B tools.

**Apollo technographic search steps:**
1. People → Search → Advanced Filters → Technologies Used
2. Enter: "HubSpot" → add filter "Technologies NOT Used" → "Lemlist"
3. This builds the exact list of HubSpot users without cold email tools
4. 10-200 employees → Series A/B funded → Export CSV
5. Apollo includes verified emails — no separate enrichment needed

**Top technographic filters available in Apollo:**
- HubSpot, Salesforce, Pipedrive (CRM presence)
- Shopify, WooCommerce, Magento (ecom)
- WordPress, Webflow, Squarespace (site builder)
- Klaviyo, Mailchimp, ActiveCampaign (email marketing)
- Google Analytics, Segment, Mixpanel (analytics)
- Stripe, Braintree (payment processor = funded)

---

## Pre-Built Lead List Sources (Skip Research Entirely)

These companies sell pre-built technographic lists:

| Source | What They Sell | Cost |
|--------|---------------|------|
| BuiltWith.com | All users of specific technology | $295/mo unlimited |
| Datanyze | Technographic data + contact info | $21-55/mo |
| Clearbit | Real-time enrichment API | $99/mo+ |
| ZoomInfo | Full B2B database with tech data | $15K+/yr (enterprise) |
| SalesIntel | Similar to ZoomInfo | $99/mo+ |

**Best for bootstrapped operation:** Apollo at $49/mo covers 80% of use cases. Only upgrade to BuiltWith once you're spending 10+ hours/week on lead research and have proven ROI.

---

## QA Checklist Before Sending Any Tech-Triggered Email

- [ ] Verified the tech stack is current (Wappalyzer data can be 30-60 days stale)
- [ ] Confirmed the company still appears to be using the tool (check their site manually for top 10 Tier 1 leads)
- [ ] Email personalization references the specific tool name, not a category
- [ ] Copy explains the gap, not just "I noticed you use X"
- [ ] Unsubscribe link in footer
- [ ] Sending from warmed domain (60+ days warm, 30 emails/day ramp)
- [ ] Under 50 emails/day per inbox until 90-day warmup complete

---

## Revenue Math

Scenario: sell cold email setup service at $1,500 flat + $500/mo retainer

| Metric | Conservative | Optimistic |
|--------|-------------|------------|
| Leads enriched/week | 500 | 2,000 |
| Reply rate (tech-triggered) | 3% | 6% |
| Replies/week | 15 | 120 |
| Meeting book rate | 25% | 40% |
| Meetings/week | 4 | 48 |
| Close rate | 20% | 35% |
| New clients/week | 0.8 | 17 |
| Monthly new clients | 3 | 68 |
| Revenue/month (new + retainers) | $4,500+ | $102K+ |

Tech-triggered cold email converts at 2-3x generic outreach. The Wappalyzer step is not optional.
