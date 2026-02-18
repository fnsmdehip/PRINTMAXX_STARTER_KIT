#!/usr/bin/env python3
"""
Voicemail Drop Campaign Manager
Source: @pipelineabuser tweet - "voicemail drops are underrated. your message lands in voicemail
without their phone ever ringing. drop.co and voicedrop.ai both do this."

Manages voicemail drop campaigns: creates scripts, tracks leads, generates reports.
Integrates with drop.co and voicedrop.ai APIs when configured.

Usage:
    python3 voicemail_drop_system.py --generate-scripts       # Generate VM scripts
    python3 voicemail_drop_system.py --prepare-campaign        # Prepare campaign from leads
    python3 voicemail_drop_system.py --summary                 # Campaign stats
"""

import argparse
import csv
import json
import os
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SCRIPTS_DIR = BASE_DIR / "AUTOMATIONS" / "voicemail_scripts"
CAMPAIGNS_CSV = BASE_DIR / "LEDGER" / "VOICEMAIL_CAMPAIGNS.csv"
LOG_FILE = BASE_DIR / "AUTOMATIONS" / "logs" / "voicemail_drops.log"

# Voicemail scripts by industry (30 seconds max each)
VM_SCRIPTS = {
    "local_biz_web_redesign": {
        "target": "Local businesses with outdated websites",
        "script": """Hey {first_name}, this is [YOUR NAME].

I was looking at {business_name}'s website and noticed a few things that might be costing you leads. Specifically, your site isn't showing up well on mobile, and there are some quick fixes that could help you rank higher on Google.

I've already put together a free audit showing exactly what to fix. No catch, just want to show you what I found.

I'll shoot you an email with the details. If you want to chat, my number is [YOUR NUMBER]. Talk soon.""",
        "duration": "28 seconds",
        "follow_up": "Send email with website audit within 2 hours",
    },
    "ecom_growth": {
        "target": "Shopify store owners doing $1M+",
        "script": """Hey {first_name}, this is [YOUR NAME].

I noticed {business_name} is doing well on Shopify. I work with ecom brands at your stage and there's usually a 15-20% revenue bump we can unlock just by optimizing your email flows and checkout.

I put together a quick analysis of your store - no charge. Just wanted to share what I found.

Sending it to your email now. If any of it resonates, happy to walk through it. My number is [YOUR NUMBER].""",
        "duration": "26 seconds",
        "follow_up": "Send email with store analysis within 2 hours",
    },
    "saas_services": {
        "target": "SaaS companies hiring engineers",
        "script": """Hey {first_name}, this is [YOUR NAME].

Saw {business_name} is hiring for {role}. Usually when teams scale that fast, documentation and internal tools become the bottleneck.

We help companies like yours build internal tools and documentation 5x faster using AI. Sounds crazy but I can show you examples.

I'll send you a quick case study. My number is [YOUR NUMBER] if you want to chat.""",
        "duration": "25 seconds",
        "follow_up": "Send email with case study within 2 hours",
    },
    "gov_contractor": {
        "target": "Small government contractors",
        "script": """Hey {first_name}, this is [YOUR NAME].

I help small contractors like {business_name} find and win government contracts. Saw you're registered on SAM but might not be seeing all the opportunities in your NAICS codes.

I put together a list of 5 active contracts you might qualify for. No charge.

Sending it over now. If you want to chat about any of them, I'm at [YOUR NUMBER].""",
        "duration": "24 seconds",
        "follow_up": "Send email with opportunity list within 2 hours",
    },
}


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_msg = f"[{timestamp}] {msg}"
    print(log_msg)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(log_msg + "\n")


def generate_scripts():
    """Generate voicemail scripts to files."""
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"VOICEMAIL DROP SCRIPTS")
    print(f"Source: @pipelineabuser - voicemail drops")
    print(f"{'='*60}\n")

    for name, data in VM_SCRIPTS.items():
        filepath = SCRIPTS_DIR / f"{name}.txt"
        content = f"""VOICEMAIL SCRIPT: {name.upper().replace('_', ' ')}
Target: {data['target']}
Duration: {data['duration']}
Follow-up: {data['follow_up']}

{'='*50}

{data['script']}

{'='*50}

RECORDING TIPS:
- Record in a quiet room
- Speak naturally, not scripted
- Smile while talking (it shows in voice)
- Keep under 30 seconds
- End with your phone number (spoken slowly)

TOOLS:
- drop.co - voicemail drops at scale
- voicedrop.ai - AI-powered voicemail drops
- Both let you upload a list and send thousands of voicemails in a day
- Average cost: $0.05-0.15 per drop

CADENCE:
- Day 1: Voicemail drop + email
- Day 3: Follow-up email with value
- Day 7: Second voicemail (different script)
- Day 14: Final email with scarcity
"""
        with open(filepath, "w") as f:
            f.write(content)
        print(f"  Created: {filepath}")
        print(f"  Target: {data['target']}")
        print(f"  Duration: {data['duration']}")
        print()

    print(f"All scripts saved to: {SCRIPTS_DIR}")
    print(f"\nNext steps:")
    print(f"  1. Record each script (use Voice Memos app)")
    print(f"  2. Sign up at drop.co or voicedrop.ai")
    print(f"  3. Upload lead list from LEDGER/LOCAL_BIZ_LEADS.csv")
    print(f"  4. Schedule drops for Tuesday-Thursday, 10am-2pm local time")


def prepare_campaign(lead_file=None):
    """Prepare a voicemail campaign from lead CSV."""
    if lead_file is None:
        lead_file = BASE_DIR / "LEDGER" / "LOCAL_BIZ_LEADS.csv"

    if not lead_file.exists():
        print(f"Lead file not found: {lead_file}")
        print("Run hexomatic_lead_gen.py first to generate leads.")
        return

    with open(lead_file, "r") as f:
        leads = list(csv.DictReader(f))

    # Filter leads with phone numbers
    with_phone = [l for l in leads if l.get("phone")]
    without_phone = [l for l in leads if not l.get("phone")]

    print(f"\n{'='*60}")
    print(f"VOICEMAIL CAMPAIGN PREP")
    print(f"{'='*60}")
    print(f"Total leads: {len(leads)}")
    print(f"With phone: {len(with_phone)} (ready for VM drops)")
    print(f"Without phone: {len(without_phone)} (need enrichment)")

    # Create campaign CSV for drop.co/voicedrop.ai upload
    campaign_file = BASE_DIR / "AUTOMATIONS" / "voicemail_scripts" / "campaign_upload.csv"
    SCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

    with open(campaign_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Phone Number", "First Name", "Business Name", "Category", "City"])
        for lead in with_phone:
            phone = lead.get("phone", "").strip()
            # Clean phone number
            phone = "".join(c for c in phone if c.isdigit())
            if len(phone) == 10:
                phone = "1" + phone
            writer.writerow([
                phone,
                lead.get("business_name", "").split()[0] if lead.get("business_name") else "",
                lead.get("business_name", ""),
                lead.get("category", ""),
                lead.get("city", ""),
            ])

    print(f"\nCampaign file: {campaign_file}")
    print(f"Ready to upload to drop.co or voicedrop.ai")

    # Track campaign
    CAMPAIGNS_CSV.parent.mkdir(parents=True, exist_ok=True)
    campaign_exists = CAMPAIGNS_CSV.exists()
    with open(CAMPAIGNS_CSV, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "campaign_id", "date", "leads_count", "leads_with_phone",
            "script_used", "tool", "status", "drops_sent", "callbacks", "meetings_booked", "notes"
        ])
        if not campaign_exists:
            writer.writeheader()
        writer.writerow({
            "campaign_id": f"VM_{datetime.now().strftime('%Y%m%d_%H%M')}",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "leads_count": len(leads),
            "leads_with_phone": len(with_phone),
            "script_used": "",
            "tool": "",
            "status": "PREPARED",
            "drops_sent": 0,
            "callbacks": 0,
            "meetings_booked": 0,
            "notes": f"Campaign file at {campaign_file}",
        })


def main():
    parser = argparse.ArgumentParser(description="Voicemail Drop Campaign Manager")
    parser.add_argument("--generate-scripts", action="store_true", help="Generate VM scripts")
    parser.add_argument("--prepare-campaign", action="store_true", help="Prepare campaign from leads")
    parser.add_argument("--lead-file", type=str, help="Path to leads CSV")
    parser.add_argument("--summary", action="store_true", help="Campaign summary")
    args = parser.parse_args()

    if args.generate_scripts:
        generate_scripts()
    elif args.prepare_campaign:
        lead_file = Path(args.lead_file) if args.lead_file else None
        prepare_campaign(lead_file)
    elif args.summary:
        if CAMPAIGNS_CSV.exists():
            with open(CAMPAIGNS_CSV, "r") as f:
                campaigns = list(csv.DictReader(f))
                print(f"\nVoicemail Campaigns: {len(campaigns)}")
                for c in campaigns:
                    print(f"  [{c.get('status')}] {c.get('date')} - {c.get('leads_with_phone')} drops")
        else:
            print("No campaigns yet.")
    else:
        generate_scripts()
        print("\nUse --prepare-campaign to create a campaign from leads.")


if __name__ == "__main__":
    main()
