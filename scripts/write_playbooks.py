#!/usr/bin/env python3
"""Generate all implementation playbooks for PRINTMAXX money methods."""
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASE = str(PROJECT_ROOT / "MONEY_METHODS")

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f'  Created: {path}')

def app_factory():
    write_file(os.path.join(BASE, 'APP_FACTORY', 'IMPLEMENTATION_PLAYBOOK.md'), APP_FACTORY_CONTENT)
    write_file(os.path.join(BASE, 'APP_FACTORY', 'QUICK_START_CHECKLIST.md'), APP_FACTORY_QS)

def cold_outbound():
    write_file(os.path.join(BASE, 'COLD_OUTBOUND', 'IMPLEMENTATION_PLAYBOOK.md'), COLD_OUTBOUND_CONTENT)
    write_file(os.path.join(BASE, 'COLD_OUTBOUND', 'QUICK_START_CHECKLIST.md'), COLD_OUTBOUND_QS)

def content_farm():
    write_file(os.path.join(BASE, 'CONTENT_FARM', 'IMPLEMENTATION_PLAYBOOK.md'), CONTENT_FARM_CONTENT)
    write_file(os.path.join(BASE, 'CONTENT_FARM', 'QUICK_START_CHECKLIST.md'), CONTENT_FARM_QS)

def ai_influencer():
    write_file(os.path.join(BASE, 'AI_INFLUENCER', 'IMPLEMENTATION_PLAYBOOK.md'), AI_INFLUENCER_CONTENT)
    write_file(os.path.join(BASE, 'AI_INFLUENCER', 'QUICK_START_CHECKLIST.md'), AI_INFLUENCER_QS)

def notion_templates():
    write_file(os.path.join(BASE, 'NOTION_TEMPLATES', 'IMPLEMENTATION_PLAYBOOK.md'), NOTION_CONTENT)

def newsletter():
    write_file(os.path.join(BASE, 'NEWSLETTER', 'IMPLEMENTATION_PLAYBOOK.md'), NEWSLETTER_CONTENT)

def info_products():
    write_file(os.path.join(BASE, 'INFO_PRODUCTS', 'IMPLEMENTATION_PLAYBOOK.md'), INFO_PRODUCTS_CONTENT)

def web_to_app():
    write_file(os.path.join(BASE, 'WEB_TO_APP_FUNNEL', 'IMPLEMENTATION_PLAYBOOK.md'), WEB_TO_APP_CONTENT)

def ai_automation():
    write_file(os.path.join(BASE, 'AI_AUTOMATION_AGENCY', 'IMPLEMENTATION_PLAYBOOK.md'), AI_AGENCY_CONTENT)

def tiktok_shop():
    write_file(os.path.join(BASE, 'TIKTOK_SHOP', 'IMPLEMENTATION_PLAYBOOK.md'), TIKTOK_CONTENT)

def portfolio_apps():
    write_file(os.path.join(BASE, 'PORTFOLIO_APP_BUILDER', 'IMPLEMENTATION_PLAYBOOK.md'), PORTFOLIO_CONTENT)

def digital_products():
    write_file(os.path.join(BASE, 'DIGITAL_PRODUCTS', 'IMPLEMENTATION_PLAYBOOK.md'), DIGITAL_CONTENT)

def x_launch():
    write_file(os.path.join(BASE, 'X_LAUNCH_VIRAL', 'IMPLEMENTATION_PLAYBOOK.md'), X_LAUNCH_CONTENT)

def course_creator():
    write_file(os.path.join(BASE, 'COURSE_CREATOR', 'IMPLEMENTATION_PLAYBOOK.md'), COURSE_CONTENT)

# Content is defined in separate data file
# For now, just print placeholder
if __name__ == '__main__':
    print("Playbook generator ready. Run with content definitions.")
