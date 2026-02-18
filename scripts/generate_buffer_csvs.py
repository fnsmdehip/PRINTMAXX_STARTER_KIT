#!/usr/bin/env python3
"""
Generate Buffer-compatible CSV files from CONTENT_CALENDAR_30DAY.csv

Splits master calendar into 12 platform-specific files for Buffer upload:
- 3 niches (faith, fitness, tech)
- 4 platforms (twitter, tiktok, instagram, linkedin)

Output: LEDGER/buffer_import_{niche}_{platform}.csv
"""

import csv
import os
from pathlib import Path

def main():
    # File paths
    base_dir = Path(__file__).parent.parent
    master_file = base_dir / 'LEDGER' / 'CONTENT_CALENDAR_30DAY.csv'
    output_dir = base_dir / 'LEDGER'

    # Check if master file exists
    if not master_file.exists():
        print(f"Error: Master calendar not found at {master_file}")
        return

    # Read master calendar
    print(f"Reading master calendar from {master_file}...")
    with open(master_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        all_posts = list(reader)

    print(f"Loaded {len(all_posts)} total posts")

    # Generate CSV for each niche + platform combination
    niches = ['faith', 'fitness', 'tech']
    platforms = ['twitter', 'tiktok', 'instagram', 'linkedin']

    total_files = 0
    total_posts = 0

    for niche in niches:
        for platform in platforms:
            # Filter posts
            posts = [p for p in all_posts if p['niche'] == niche and p['platform'] == platform]

            if not posts:
                print(f"Warning: No posts found for {niche} + {platform}")
                continue

            # Create output file
            output_file = output_dir / f'buffer_import_{niche}_{platform}.csv'

            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                # Buffer CSV format: Date, Time, Text
                writer.writerow(['Date', 'Time', 'Text'])

                for post in posts:
                    # Combine post text + hashtags
                    text = post['post_text']

                    # Add hashtags if present
                    if post.get('hashtags'):
                        # Clean up hashtags (remove extra commas, spaces)
                        hashtags = post['hashtags'].replace(',', ' ').strip()
                        if hashtags:
                            text += '\n\n' + hashtags

                    # Add CTA if present
                    if post.get('cta'):
                        text += '\n\n' + post['cta']

                    # Add link if present (not for all platforms)
                    if post.get('link') and platform in ['twitter', 'linkedin']:
                        text += '\n\n' + post['link']

                    writer.writerow([post['date'], post['time'], text])

            print(f"✓ Created {output_file.name} ({len(posts)} posts)")
            total_files += 1
            total_posts += len(posts)

    print(f"\n✅ Success! Generated {total_files} CSV files with {total_posts} total posts")
    print(f"\nFiles created in: {output_dir}")
    print("\nNext steps:")
    print("1. Go to buffer.com (or publer.io)")
    print("2. Connect your social accounts")
    print("3. Upload each CSV file to the corresponding account")
    print("4. Verify schedule and publish")

if __name__ == '__main__':
    main()
