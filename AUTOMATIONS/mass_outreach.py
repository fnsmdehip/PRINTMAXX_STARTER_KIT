#!/usr/bin/env python3
"""
mass_outreach.py - Cold email pipeline from scraped leads

Reads CSV output from savvy_lead_scraper.py, generates personalized cold emails
using built-in industry templates (no AI needed), and exports to Instantly-compatible
CSV format for bulk sending.

10 industry-specific templates built in. 3-email sequence per lead.

Usage:
    python3 mass_outreach.py --input leads/dental_austin_tx_leads.csv --template dental
    python3 mass_outreach.py --input leads/MASTER_LEADS.csv --template auto --output outreach/master_emails.csv
    python3 mass_outreach.py --help

Output:
    Instantly-compatible CSV: AUTOMATIONS/outreach/[name]_emails.csv
    Pipeline tracker:         AUTOMATIONS/outreach/PIPELINE_TRACKER.csv

Dependencies:
    None (pure Python stdlib)
"""

import argparse
import csv
import os
import re
import sys
from datetime import datetime
from pathlib import Path


# ============================================================================
# CONSTANTS
# ============================================================================

SCRIPT_DIR = Path(__file__).parent.resolve()
OUTREACH_DIR = SCRIPT_DIR / "outreach"

INSTANTLY_HEADERS = [
    "email", "first_name", "company_name", "phone",
    "custom1_demo_url", "custom2_city", "custom3_score", "custom4_top_issue",
    "sequence_step", "send_day", "subject", "body",
]

TRACKER_HEADERS = [
    "lead_id", "business_name", "category", "city", "email", "phone",
    "website_score", "top_issue", "template_used", "sequence_emails",
    "status", "date_added", "date_sent", "date_replied", "notes",
]


# ============================================================================
# PERSONALIZATION HELPERS
# ============================================================================

def extract_first_name(business_name):
    """Try to get a first name from the business (e.g. 'Joe's Plumbing' -> 'Joe')."""
    m = re.match(r"(\w+)'s\b", business_name)
    if m:
        return m.group(1)
    m = re.match(r"Dr\.?\s+(\w+)", business_name)
    if m:
        return m.group(1)
    return "there"


def get_top_issue(signals_str):
    """Extract the most important issue from signals string."""
    signals = signals_str.lower() if signals_str else ""
    if "not_mobile" in signals or "no_viewport" in signals:
        return "not mobile-friendly"
    if "no_ssl" in signals:
        return "missing SSL certificate"
    if "very_slow" in signals or "slow:" in signals:
        return "slow page load speed"
    if "no_website" in signals or "directory_listing" in signals:
        return "no real website"
    if "old_" in signals and "(c)" in signals:
        return "outdated copyright year"
    if "bad_title" in signals or "no_desc" in signals:
        return "poor SEO setup"
    if "no_schema" in signals:
        return "missing structured data"
    if "no_form" in signals:
        return "no contact form"
    if "no_social" in signals:
        return "no social media links"
    if any(x in signals for x in ["old:fa4", "old:bs3", "old:bs2", "old:jq1"]):
        return "outdated technology stack"
    return "website needs a refresh"


def apply_template(template_str, variables):
    """Replace {{VAR}} placeholders with actual values."""
    result = template_str
    for key, value in variables.items():
        result = result.replace("{{" + key + "}}", str(value))
    return result


# ============================================================================
# 10 INDUSTRY-SPECIFIC EMAIL TEMPLATES (3-email sequence each)
# ============================================================================

# Each template has: subject, body for steps 1 (day 0), 2 (day 3), 3 (day 7)

TEMPLATES = {
    "dental": {
        "name": "Dental / Orthodontics",
        "sequences": [
            {
                "step": 1, "day": 0,
                "subject": "I noticed something about {{BUSINESS_NAME}}'s website",
                "body": """Hi {{FIRST_NAME}},

I was looking for dentists in {{CITY}} and came across {{BUSINESS_NAME}}'s website. I noticed {{TOP_ISSUE}} -- that's probably costing you new patient inquiries.

In my experience working with dental practices, fixing mobile responsiveness and basic SEO alone can increase new patient calls by 30-50%. Most people search for dentists on their phone now.

I put together a quick audit of what I found. Would it be helpful if I sent it over?

Best,
{{SENDER_NAME}}

PS - Not trying to sell you anything right now. Just genuinely noticed the issue and figured you'd want to know.""",
            },
            {
                "step": 2, "day": 3,
                "subject": "re: {{BUSINESS_NAME}} website",
                "body": """Hi {{FIRST_NAME}},

Quick follow-up on my note about {{BUSINESS_NAME}}'s website.

Here's the thing -- a dental practice in {{CITY}} getting even 200 website visitors per month with a {{WEBSITE_SCORE}}/100 quality score is probably converting at 1-2% into calls. Fix the issues I found and that goes to 4-6%.

That's 4-8 more new patient calls per month. At an average patient lifetime value of $3,000-$5,000, even one extra patient a month from a better website pays for itself many times over.

Happy to walk you through the specifics. Takes 15 minutes.

{{SENDER_NAME}}""",
            },
            {
                "step": 3, "day": 7,
                "subject": "last note about {{BUSINESS_NAME}}",
                "body": """Hi {{FIRST_NAME}},

Last email from me. I just wanted to make sure you saw my note about {{BUSINESS_NAME}}'s website having {{TOP_ISSUE}}.

If you're interested in fixing it, I can have a modern, mobile-friendly version ready in 48 hours for $500 flat. Includes SEO setup, SSL, and 30 days of support.

If not, no worries at all. I hope the audit was useful regardless.

Best,
{{SENDER_NAME}}

Reply "remove" and you won't hear from me again.""",
            },
        ],
    },

    "legal": {
        "name": "Legal / Law Firms",
        "sequences": [
            {
                "step": 1, "day": 0,
                "subject": "{{BUSINESS_NAME}} -- website concern",
                "body": """Hi {{FIRST_NAME}},

I was researching law firms in {{CITY}} and noticed {{BUSINESS_NAME}}'s website has {{TOP_ISSUE}}. For a law firm, this is particularly important because potential clients are comparing you to competitors right now.

70% of people looking for a lawyer will visit 2-3 firm websites before calling. If yours looks dated or doesn't work on mobile, they'll call the firm whose site looked more professional.

Would it be worth a 10-minute call to discuss what I found?

{{SENDER_NAME}}""",
            },
            {
                "step": 2, "day": 3,
                "subject": "re: {{BUSINESS_NAME}} website",
                "body": """Hi {{FIRST_NAME}},

Following up on my note about {{BUSINESS_NAME}}'s website. Your site scored {{WEBSITE_SCORE}}/100 on our quality assessment.

The main issues: {{TOP_ISSUE}}. For legal services where average case values run $3,000-$10,000, every lost inquiry from a poor website experience is significant.

I rebuild law firm websites all the time. $500 flat, 48 hours, includes mobile optimization, proper legal schema markup for Google, and SSL.

Worth a quick conversation?

{{SENDER_NAME}}""",
            },
            {
                "step": 3, "day": 7,
                "subject": "closing the loop on {{BUSINESS_NAME}}",
                "body": """Hi {{FIRST_NAME}},

Last email from me about {{BUSINESS_NAME}}'s website.

Quick summary: your site has {{TOP_ISSUE}}, which is likely costing you clients. I can fix it for $500 in 48 hours.

If you'd rather handle it yourself, the top 3 things to fix are: mobile responsiveness, page speed, and Google schema markup for local business.

Either way, I hope this was helpful.

{{SENDER_NAME}}

Reply "remove" to unsubscribe.""",
            },
        ],
    },

    "restaurant": {
        "name": "Restaurant / Cafe",
        "sequences": [
            {
                "step": 1, "day": 0,
                "subject": "quick note about {{BUSINESS_NAME}}'s online presence",
                "body": """Hi {{FIRST_NAME}},

I was looking for places to eat in {{CITY}} and found {{BUSINESS_NAME}}. Your food looks great, but I noticed your website has {{TOP_ISSUE}}.

86% of diners check a restaurant's website before visiting. If yours isn't mobile-friendly or loads slowly, you're losing customers to the place down the street.

I've helped restaurants in {{CITY}} modernize their sites. Quick fix, big impact.

Would you be interested in seeing what a refreshed version could look like?

{{SENDER_NAME}}""",
            },
            {
                "step": 2, "day": 3,
                "subject": "re: {{BUSINESS_NAME}} website",
                "body": """Hi {{FIRST_NAME}},

Following up about {{BUSINESS_NAME}}'s website (scored {{WEBSITE_SCORE}}/100).

For restaurants, the #1 thing that matters is: can someone on their phone see your menu, hours, and location in under 3 seconds? Right now, {{TOP_ISSUE}} is getting in the way of that.

I can build you a clean, fast, mobile-first site for $500. Menu, hours, location, reservation link, Google Maps -- everything a hungry customer needs.

Interested?

{{SENDER_NAME}}""",
            },
            {
                "step": 3, "day": 7,
                "subject": "last note for {{BUSINESS_NAME}}",
                "body": """Hi {{FIRST_NAME}},

Last email about your website. I know you're busy running {{BUSINESS_NAME}}.

Bottom line: {{TOP_ISSUE}} is costing you customers. I can fix it for $500, delivered in 48 hours.

If you're not ready now, at minimum make sure your menu is a real webpage (not a PDF) and your hours are up to date on Google.

Best of luck.

{{SENDER_NAME}}

Reply "remove" to opt out.""",
            },
        ],
    },

    "plumbing": {
        "name": "Plumbing",
        "sequences": [
            {
                "step": 1, "day": 0,
                "subject": "{{BUSINESS_NAME}} -- losing leads to competitors?",
                "body": """Hi {{FIRST_NAME}},

I was looking at plumbing companies in {{CITY}} and noticed {{BUSINESS_NAME}}'s website has {{TOP_ISSUE}}.

When someone's toilet is overflowing at 11pm, they're searching on their phone. If your site doesn't load fast and work on mobile, they're calling the next plumber in the list.

I've seen this pattern with a lot of local service businesses. The fix is straightforward and the ROI is fast.

Would a quick chat be worth your time?

{{SENDER_NAME}}""",
            },
            {
                "step": 2, "day": 3,
                "subject": "re: {{BUSINESS_NAME}} website",
                "body": """Hi {{FIRST_NAME}},

Your website scored {{WEBSITE_SCORE}}/100 on quality. Main issue: {{TOP_ISSUE}}.

For a plumbing company, every missed web lead costs $500-$2,000 in lost revenue. Fix the site, same Google traffic converts into 2-3x more calls.

I do this for $500 flat. 48 hours. Mobile-optimized, fast, with a click-to-call button front and center.

Worth discussing?

{{SENDER_NAME}}""",
            },
            {
                "step": 3, "day": 7,
                "subject": "last note - {{BUSINESS_NAME}}",
                "body": """Hi {{FIRST_NAME}},

Final follow-up about {{BUSINESS_NAME}}'s website.

The main issue ({{TOP_ISSUE}}) is fixable. $500, 48 hours, includes mobile optimization and SEO basics.

If you handle your own website, the #1 thing to fix is making sure your phone number is clickable on mobile and loads above the fold.

Best,
{{SENDER_NAME}}

Reply "remove" to unsubscribe.""",
            },
        ],
    },

    "hvac": {
        "name": "HVAC / Heating & Cooling",
        "sequences": [
            {
                "step": 1, "day": 0,
                "subject": "{{BUSINESS_NAME}} -- summer is coming",
                "body": """Hi {{FIRST_NAME}},

I was looking at HVAC companies in {{CITY}} and noticed {{BUSINESS_NAME}}'s website has {{TOP_ISSUE}}.

With AC season approaching, you'll see a surge in emergency searches. People with a broken AC at 2pm on a Saturday aren't patient -- they'll call whichever company's website loads fast and has a phone number they can click.

Is your site ready for that surge?

I help HVAC companies modernize their websites. Happy to discuss.

{{SENDER_NAME}}""",
            },
            {
                "step": 2, "day": 3,
                "subject": "re: {{BUSINESS_NAME}} website",
                "body": """Hi {{FIRST_NAME}},

Your site scored {{WEBSITE_SCORE}}/100. The main issue: {{TOP_ISSUE}}.

For HVAC companies, average job value is $1,500-$3,000. If a better website gets you even 2 more calls per month, that's $3,000-$6,000 in additional revenue.

The fix: $500 for a modern, mobile-first site with click-to-call, service area pages, and proper local SEO. Delivered in 48 hours.

Worth a conversation?

{{SENDER_NAME}}""",
            },
            {
                "step": 3, "day": 7,
                "subject": "last email - {{BUSINESS_NAME}}",
                "body": """Hi {{FIRST_NAME}},

Last email from me. {{BUSINESS_NAME}}'s website has {{TOP_ISSUE}} and it's likely costing you emergency service calls.

$500 to fix. 48 hours. No ongoing fees unless you want monthly maintenance.

Either way, make sure your phone number is prominently displayed and clickable on mobile before busy season hits.

{{SENDER_NAME}}

Reply "remove" to opt out.""",
            },
        ],
    },

    "real_estate": {
        "name": "Real Estate",
        "sequences": [
            {
                "step": 1, "day": 0,
                "subject": "{{BUSINESS_NAME}} -- your listings deserve better",
                "body": """Hi {{FIRST_NAME}},

I came across {{BUSINESS_NAME}} while looking at real estate agents in {{CITY}}. Your listings look great, but your website has {{TOP_ISSUE}}.

In real estate, your website IS your storefront. Buyers and sellers are comparing agents online before they ever pick up the phone. A dated or slow site signals "part-time agent" even if you're anything but.

Would you be open to seeing what a modernized version could look like?

{{SENDER_NAME}}""",
            },
            {
                "step": 2, "day": 3,
                "subject": "re: {{BUSINESS_NAME}} website",
                "body": """Hi {{FIRST_NAME}},

Your site scored {{WEBSITE_SCORE}}/100. Main issue: {{TOP_ISSUE}}.

In a market where one closed deal is $5,000-$15,000 in commission, your website needs to work for you 24/7. Right now, it might be working against you.

I build clean, fast, mobile-first sites for real estate professionals. $500, 48 hours, includes IDX-ready design and local SEO.

Worth a quick call?

{{SENDER_NAME}}""",
            },
            {
                "step": 3, "day": 7,
                "subject": "closing the loop - {{BUSINESS_NAME}}",
                "body": """Hi {{FIRST_NAME}},

Last note about your website. The issue ({{TOP_ISSUE}}) is costing you leads to agents with better sites.

$500 to fix. 48 hours turnaround. Includes mobile optimization, proper local SEO, and a design that matches the quality of your listings.

Hope to hear from you, but either way I wish you a strong selling season.

{{SENDER_NAME}}

Reply "remove" to unsubscribe.""",
            },
        ],
    },

    "fitness": {
        "name": "Gym / Fitness Studio",
        "sequences": [
            {
                "step": 1, "day": 0,
                "subject": "{{BUSINESS_NAME}} -- website check",
                "body": """Hi {{FIRST_NAME}},

I was checking out fitness options in {{CITY}} and found {{BUSINESS_NAME}}. Looks like a great spot, but your website has {{TOP_ISSUE}}.

People searching for gyms are comparing 3-4 options before visiting. If your site is slow or doesn't work on mobile, they'll sign up at the studio down the street -- even if your classes are better.

I help fitness businesses fix exactly this. Quick chat worth your time?

{{SENDER_NAME}}""",
            },
            {
                "step": 2, "day": 3,
                "subject": "re: {{BUSINESS_NAME}} website",
                "body": """Hi {{FIRST_NAME}},

Site score: {{WEBSITE_SCORE}}/100. Main issue: {{TOP_ISSUE}}.

At $50-$150/month per member, every signup you miss because of a bad website adds up fast. 5 lost signups = $3,000-$9,000/year in recurring revenue gone.

Fix: $500, 48 hours. Clean schedule display, class booking integration, mobile-first, SEO basics.

Interested?

{{SENDER_NAME}}""",
            },
            {
                "step": 3, "day": 7,
                "subject": "last one - {{BUSINESS_NAME}}",
                "body": """Hi {{FIRST_NAME}},

Final email. Your site has {{TOP_ISSUE}} and it's likely costing you member signups.

$500 fix, 48 hours. Mobile-first, fast-loading, with your schedule and pricing front and center.

Good luck with {{BUSINESS_NAME}}.

{{SENDER_NAME}}

Reply "remove" to opt out.""",
            },
        ],
    },

    "salon": {
        "name": "Salon / Spa",
        "sequences": [
            {
                "step": 1, "day": 0,
                "subject": "{{BUSINESS_NAME}} -- website first impression",
                "body": """Hi {{FIRST_NAME}},

I found {{BUSINESS_NAME}} while looking for salons in {{CITY}}. Your reviews are great, but your website has {{TOP_ISSUE}}.

For a salon, your website is the first impression. If it looks dated, people assume the salon is too. Your Google reviews say otherwise, but not everyone reads those first.

Would you want to see what a modern version could look like? No cost for the mockup.

{{SENDER_NAME}}""",
            },
            {
                "step": 2, "day": 3,
                "subject": "re: {{BUSINESS_NAME}} website",
                "body": """Hi {{FIRST_NAME}},

Your site scored {{WEBSITE_SCORE}}/100. Issue: {{TOP_ISSUE}}.

A modern salon website with online booking, service menu, and gallery photos converts visitors into appointments at 3-5x the rate of a dated site.

I can build this for $500, delivered in 48 hours. Clean, beautiful, mobile-first.

Worth discussing?

{{SENDER_NAME}}""",
            },
            {
                "step": 3, "day": 7,
                "subject": "last note - {{BUSINESS_NAME}}",
                "body": """Hi {{FIRST_NAME}},

Final follow-up. {{TOP_ISSUE}} on your site is likely turning away potential clients.

$500 to fix. 48 hours. Beautiful mobile design that matches the quality of your work.

Best wishes to you and the team at {{BUSINESS_NAME}}.

{{SENDER_NAME}}

Reply "remove" to unsubscribe.""",
            },
        ],
    },

    "auto_repair": {
        "name": "Auto Repair / Mechanic",
        "sequences": [
            {
                "step": 1, "day": 0,
                "subject": "{{BUSINESS_NAME}} -- website question",
                "body": """Hi {{FIRST_NAME}},

I was looking for mechanics in {{CITY}} and found {{BUSINESS_NAME}}. Your reviews look solid, but your website has {{TOP_ISSUE}}.

When someone's car breaks down, they search on their phone. If your website doesn't load or work on mobile, they go to the shop with the better-looking site. Even if you're the better mechanic.

I fix websites for auto shops. Simple, fast, affordable. Worth a chat?

{{SENDER_NAME}}""",
            },
            {
                "step": 2, "day": 3,
                "subject": "re: {{BUSINESS_NAME}} website",
                "body": """Hi {{FIRST_NAME}},

Site quality: {{WEBSITE_SCORE}}/100. Main issue: {{TOP_ISSUE}}.

Average auto repair ticket is $300-$1,500. A modern site that converts even 2 more walk-ins per month pays for itself immediately.

$500. 48 hours. Mobile-first with click-to-call, services list, and Google Maps embedded.

Let me know if you're interested.

{{SENDER_NAME}}""",
            },
            {
                "step": 3, "day": 7,
                "subject": "last email - {{BUSINESS_NAME}}",
                "body": """Hi {{FIRST_NAME}},

Last one from me. {{BUSINESS_NAME}}'s website needs {{TOP_ISSUE}} fixed.

$500, 48 hours, no ongoing costs. Let me know if you'd like to proceed.

Best,
{{SENDER_NAME}}

Reply "remove" to opt out.""",
            },
        ],
    },

    "accounting": {
        "name": "Accounting / CPA",
        "sequences": [
            {
                "step": 1, "day": 0,
                "subject": "{{BUSINESS_NAME}} -- website audit",
                "body": """Hi {{FIRST_NAME}},

I was researching accounting firms in {{CITY}} and noticed {{BUSINESS_NAME}}'s website has {{TOP_ISSUE}}.

For a professional services firm, your website signals credibility. A dated site raises trust concerns -- especially when people are looking for someone to handle their finances.

I've helped accounting firms modernize their web presence. Would a brief conversation be valuable?

{{SENDER_NAME}}""",
            },
            {
                "step": 2, "day": 3,
                "subject": "re: {{BUSINESS_NAME}} website",
                "body": """Hi {{FIRST_NAME}},

Site score: {{WEBSITE_SCORE}}/100. Issue: {{TOP_ISSUE}}.

With tax season approaching, your website traffic will spike. A client worth $1,000-$5,000/year in recurring fees makes every conversion matter.

I build professional, clean sites for accounting firms. $500 flat, 48 hours, includes mobile optimization and local SEO.

Worth discussing?

{{SENDER_NAME}}""",
            },
            {
                "step": 3, "day": 7,
                "subject": "last note - {{BUSINESS_NAME}}",
                "body": """Hi {{FIRST_NAME}},

Final follow-up. Your site has {{TOP_ISSUE}} and tax season traffic is coming.

$500 to fix. 48 hours. Professional design that matches the caliber of your firm.

Best regards,
{{SENDER_NAME}}

Reply "remove" to unsubscribe.""",
            },
        ],
    },
}

# Auto-detect template based on category keywords
TEMPLATE_ALIASES = {
    "dental": "dental", "dentist": "dental", "orthodont": "dental",
    "legal": "legal", "lawyer": "legal", "attorney": "legal", "law": "legal",
    "restaurant": "restaurant", "cafe": "restaurant", "diner": "restaurant",
    "plumbing": "plumbing", "plumber": "plumbing",
    "hvac": "hvac", "heating": "hvac", "cooling": "hvac", "air condition": "hvac",
    "real_estate": "real_estate", "realtor": "real_estate", "real estate": "real_estate",
    "fitness": "fitness", "gym": "fitness", "yoga": "fitness", "crossfit": "fitness",
    "salon": "salon", "spa": "salon", "beauty": "salon", "hair": "salon", "nail": "salon",
    "auto_repair": "auto_repair", "auto repair": "auto_repair", "mechanic": "auto_repair",
    "accounting": "accounting", "accountant": "accounting", "cpa": "accounting", "tax": "accounting",
}


def detect_template(category_or_name):
    """Auto-detect the best template for a category string."""
    key = category_or_name.lower().strip()
    # Direct match
    if key in TEMPLATES:
        return key
    # Alias match
    for alias, tmpl in TEMPLATE_ALIASES.items():
        if alias in key:
            return tmpl
    # Default
    return "plumbing"  # Generic service template works for most


# ============================================================================
# EMAIL GENERATION
# ============================================================================

def generate_emails_for_lead(lead, template_key, sender_name="Sarah"):
    """Generate a 3-email sequence for a single lead."""
    tmpl = TEMPLATES.get(template_key, TEMPLATES["plumbing"])
    biz_name = lead.get("business_name", "Your Business")
    first_name = extract_first_name(biz_name)
    city = lead.get("city", "your area")
    score = lead.get("website_score", "50")
    signals = lead.get("signals_detected", "")
    top_issue = get_top_issue(signals)
    email_addr = lead.get("email_if_found", "").split(";")[0].strip()

    variables = {
        "BUSINESS_NAME": biz_name,
        "FIRST_NAME": first_name,
        "CITY": city,
        "WEBSITE_SCORE": str(score),
        "TOP_ISSUE": top_issue,
        "SENDER_NAME": sender_name,
        "OWNER_NAME": first_name if first_name != "there" else "Owner",
    }

    emails = []
    for seq in tmpl["sequences"]:
        emails.append({
            "email": email_addr,
            "first_name": first_name,
            "company_name": biz_name,
            "phone": lead.get("phone", ""),
            "custom1_demo_url": "",
            "custom2_city": city,
            "custom3_score": str(score),
            "custom4_top_issue": top_issue,
            "sequence_step": seq["step"],
            "send_day": seq["day"],
            "subject": apply_template(seq["subject"], variables),
            "body": apply_template(seq["body"], variables),
        })
    return emails


# ============================================================================
# PIPELINE TRACKER
# ============================================================================

def write_tracker(leads, template_key, tracker_path):
    """Write the PIPELINE_TRACKER.csv."""
    with open(tracker_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=TRACKER_HEADERS)
        w.writeheader()
        for i, lead in enumerate(leads, 1):
            signals = lead.get("signals_detected", "")
            w.writerow({
                "lead_id": f"L-{i:05d}",
                "business_name": lead.get("business_name", ""),
                "category": lead.get("category", ""),
                "city": lead.get("city", ""),
                "email": lead.get("email_if_found", "").split(";")[0].strip(),
                "phone": lead.get("phone", ""),
                "website_score": lead.get("website_score", ""),
                "top_issue": get_top_issue(signals),
                "template_used": template_key,
                "sequence_emails": 3,
                "status": "READY",
                "date_added": datetime.now().strftime("%Y-%m-%d"),
                "date_sent": "",
                "date_replied": "",
                "notes": "",
            })


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def run_outreach(input_csv, template_key, output_csv=None, sender_name="Sarah",
                 auto_detect=False, min_score=0, max_leads=0):
    """Main outreach pipeline."""
    OUTREACH_DIR.mkdir(parents=True, exist_ok=True)

    # Load leads
    with open(input_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        all_leads = list(reader)

    print(f"\n{'='*60}")
    print(f"  MASS OUTREACH PIPELINE")
    print(f"{'='*60}")
    print(f"  Input:      {input_csv}")
    print(f"  Total leads: {len(all_leads)}")

    # Filter by email presence and score
    leads_with_email = []
    leads_without_email = []
    for lead in all_leads:
        email = lead.get("email_if_found", "").split(";")[0].strip()
        try:
            score = int(lead.get("website_score", "100"))
        except (ValueError, TypeError):
            score = 100
        if min_score > 0 and score > min_score:
            continue  # Skip leads with score above threshold (higher = better site = less need)
        if email and "@" in email:
            leads_with_email.append(lead)
        else:
            leads_without_email.append(lead)

    if max_leads > 0:
        leads_with_email = leads_with_email[:max_leads]

    print(f"  With email:  {len(leads_with_email)}")
    print(f"  No email:    {len(leads_without_email)}")
    if min_score > 0:
        print(f"  Score filter: <= {min_score}")
    print(f"  Template:    {template_key} ({TEMPLATES.get(template_key, {}).get('name', 'auto')})")
    print(f"  Sender:      {sender_name}")
    print(f"{'='*60}\n")

    if not leads_with_email:
        print("[!] No leads with email addresses found.")
        print("    Try running savvy_lead_scraper.py on more cities to find more emails.")
        return

    # Generate emails
    all_email_rows = []
    for lead in leads_with_email:
        if auto_detect:
            cat = lead.get("category", "")
            tk = detect_template(cat) if cat else template_key
        else:
            tk = template_key
        emails = generate_emails_for_lead(lead, tk, sender_name=sender_name)
        all_email_rows.extend(emails)

    # Output path
    if not output_csv:
        stem = Path(input_csv).stem
        output_csv = OUTREACH_DIR / f"{stem}_emails.csv"
    else:
        output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    # Write Instantly-compatible CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=INSTANTLY_HEADERS)
        w.writeheader()
        w.writerows(all_email_rows)

    # Write per-step CSVs
    for step in [1, 2, 3]:
        step_rows = [r for r in all_email_rows if r["sequence_step"] == step]
        if step_rows:
            step_path = output_csv.parent / f"{output_csv.stem}_step{step}.csv"
            with open(step_path, "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=INSTANTLY_HEADERS)
                w.writeheader()
                w.writerows(step_rows)

    # Write pipeline tracker
    tracker_path = OUTREACH_DIR / "PIPELINE_TRACKER.csv"
    write_tracker(leads_with_email, template_key, tracker_path)

    # Summary
    print(f"{'='*60}")
    print(f"  OUTREACH COMPLETE")
    print(f"{'='*60}")
    print(f"  Leads processed:  {len(leads_with_email)}")
    print(f"  Total emails:     {len(all_email_rows)} ({len(leads_with_email)} x 3 steps)")
    print(f"  Step 1 (day 0):   {sum(1 for r in all_email_rows if r['sequence_step'] == 1)} emails")
    print(f"  Step 2 (day 3):   {sum(1 for r in all_email_rows if r['sequence_step'] == 2)} emails")
    print(f"  Step 3 (day 7):   {sum(1 for r in all_email_rows if r['sequence_step'] == 3)} emails")
    print()
    print(f"  Output files:")
    print(f"    Full batch:    {output_csv}")
    print(f"    Step 1 CSV:    {output_csv.parent / f'{output_csv.stem}_step1.csv'}")
    print(f"    Step 2 CSV:    {output_csv.parent / f'{output_csv.stem}_step2.csv'}")
    print(f"    Step 3 CSV:    {output_csv.parent / f'{output_csv.stem}_step3.csv'}")
    print(f"    Tracker:       {tracker_path}")
    print()
    print(f"  Next steps:")
    print(f"    1. Upload to Instantly: {output_csv}")
    print(f"    2. Set sequence: Step 1 on day 0, Step 2 on day 3, Step 3 on day 7")
    print(f"    3. Start at 10 emails/day, ramp to 50 after warmup")
    print(f"    4. Track replies in: {tracker_path}")
    print(f"{'='*60}\n")


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Mass Outreach - Cold email pipeline from scraped leads",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 mass_outreach.py --input leads/dental_austin_tx_leads.csv --template dental
  python3 mass_outreach.py --input leads/MASTER_LEADS.csv --template auto
  python3 mass_outreach.py --input leads/MASTER_LEADS.csv --template legal --output outreach/legal_emails.csv
  python3 mass_outreach.py --list-templates

Templates (10 built-in):
  dental, legal, restaurant, plumbing, hvac, real_estate, fitness, salon, auto_repair, accounting
  Use --template auto to auto-detect from the 'category' column in the CSV.

Output:
  Instantly-compatible CSV:    AUTOMATIONS/outreach/[name]_emails.csv
  Per-step CSVs:               AUTOMATIONS/outreach/[name]_emails_step1.csv (etc.)
  Pipeline tracker:            AUTOMATIONS/outreach/PIPELINE_TRACKER.csv
""")
    parser.add_argument("--input", "-i", default=None,
                        help="Input CSV from savvy_lead_scraper.py or nationwide_scraper.py")
    parser.add_argument("--template", "-t", default=None,
                        help="Template key (dental, legal, etc.) or 'auto' for auto-detect")
    parser.add_argument("--output", "-o",
                        help="Output CSV path (default: outreach/[input_name]_emails.csv)")
    parser.add_argument("--sender", default="Sarah",
                        help="Sender name for emails (default: Sarah)")
    parser.add_argument("--max-score", type=int, default=0,
                        help="Only include leads with website_score <= this (0 = all)")
    parser.add_argument("--max-leads", type=int, default=0,
                        help="Max leads to process (0 = all)")
    parser.add_argument("--list-templates", action="store_true",
                        help="List available templates and exit")

    args = parser.parse_args()

    if args.list_templates:
        print("\nAvailable templates:")
        for key, tmpl in TEMPLATES.items():
            print(f"  {key:<15} {tmpl['name']}")
        print(f"\n  Use --template auto to auto-detect from CSV 'category' column.")
        print(f"  Aliases: {', '.join(sorted(TEMPLATE_ALIASES.keys()))}\n")
        return

    if not args.input:
        parser.error("--input is required (unless using --list-templates)")
    if not args.template:
        parser.error("--template is required (unless using --list-templates)")

    auto_detect = args.template.lower() == "auto"
    template_key = detect_template(args.template) if not auto_detect else "plumbing"

    if not auto_detect and template_key not in TEMPLATES:
        print(f"[!] Unknown template: {args.template}")
        print(f"    Available: {', '.join(TEMPLATES.keys())}")
        print(f"    Or use --template auto")
        sys.exit(1)

    if not Path(args.input).exists():
        print(f"[!] Input file not found: {args.input}")
        sys.exit(1)

    run_outreach(
        input_csv=args.input,
        template_key=template_key,
        output_csv=args.output,
        sender_name=args.sender,
        auto_detect=auto_detect,
        min_score=args.max_score,
        max_leads=args.max_leads,
    )


if __name__ == "__main__":
    main()
