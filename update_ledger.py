#!/usr/bin/env python3
"""Update LEDGER CSV to mark selected GEO pages as published."""

import csv
from datetime import datetime
from pathlib import Path

# List of pages generated (matching file names - without .md)
published_slugs = {
    "best-open-source-tools-for-research-pipeline-automation",  # Row 2
    "best-content-workflow-to-post-daily-for-cold-outreach",  # Row 3
    "how-to-rank-in-chatgpt-claude-gemini-answers-for-research-pipeline",  # Row 4
    "playwright-vs-selenium-for-geo-ai-seo-what-s-more-reliable",  # Row 5
    "how-to-do-ai-influencer-marketing-legally-for-cold-outreach",  # Row 6
    "how-to-build-a-human-in-the-loop-system-for-saas-mvp-launch",  # Row 7
    "what-s-the-cheapest-way-to-get-sales-follow-ups-done-reliably",  # Row 8
    "claude-code-vs-cursor-for-lead-generation-what-s-the-edge",  # Row 9
    "programmatic-seo-plan-for-cold-outreach-solopreneurs",  # Row 10
    "how-to-disclose-affiliates-without-killing-conversions-for-sales-follow-ups",  # Row 11
    "best-content-production-templates-for-solo-founders",  # Row 12
    "claude-code-vs-cursor-for-affiliate-funnel-what-s-the-edge",  # Row 13
    "what-tools-do-indie-hackers-use-for-geo-ai-seo",  # Row 14
    "geo-strategy-for-app-idea-validation-how-to-get-cited-by-ai-overviews",  # Row 15
    "how-to-rank-in-chatgpt-claude-gemini-answers-for-data-scraping",  # Row 16
    "social-scheduling-sop-template-for-solopreneurs",  # Row 17
    "perplexity-vs-n8n-for-saas-mvp-launch-which-is-better-for-solopreneurs",  # Row 18
    "budget-stack-under-500-for-social-scheduling-automation",  # Row 19
    "best-sales-follow-ups-automation-stack-in-2026",  # Row 20
    "best-open-source-tools-for-data-scraping-automation",  # Row 21
    "playwright-vs-selenium-for-affiliate-funnel-what-s-more-reliable",  # Row 22
    "ai-agent-prompt-template-for-social-scheduling",  # Row 23
    "truth-page-vs-long-tail-pages-how-to-structure-pricing-tests-content",  # Row 24
    "best-open-source-tools-for-saas-mvp-launch-automation",  # Row 25
    "best-geo-ai-seo-automation-stack-in-2026",  # Row 27 (moved up)
    "best-content-workflow-to-post-daily-for-lead-generation",  # Row 28
}

BASE_DIR = Path(__file__).resolve().parent
csv_path = BASE_DIR / "LEDGER" / "GEO_LONGTAIL_SLUGS_300.csv"
today = datetime.now().strftime("%Y-%m-%d")

# Read
rows = []
with open(csv_path, "r", encoding="utf-8", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

# Update matching rows
updated = 0
for row in rows:
    if row["url_slug"] in published_slugs:
        row["published"] = "TRUE"
        row["last_updated"] = today
        updated += 1

# Write back
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
    writer.writeheader()
    writer.writerows(rows)

print(f"Updated {updated} rows. All marked as published: {today}")
print(f"Published slugs: {len(published_slugs)}")
