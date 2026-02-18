#!/bin/bash

# QUICK LAUNCH SETUP - Essential materials for immediate launch

TOP_10_APPS=(
    "quran-streak|Quran Streak|🕌"
    "language-streak|Language Streak|🌍"
    "fitness-streak|Fitness Streak|💪"
    "meditation-streak|Meditation Streak|🧘"
    "coding-streak|Coding Streak|💻"
    "reading-streak|Reading Streak|📚"
    "journal-streak|Journal Streak|📓"
    "spanish-streak|Spanish Streak|🇪🇸"
    "running-streak|Running Streak|🏃"
    "yoga-streak|Yoga Streak|🧘‍♀️"
)

create_launch_package() {
    local app_config=$1
    IFS='|' read -r app_name display_name icon <<< "$app_config"

    echo "📦 Creating launch essentials for $display_name..."

    # App Store Listing
    mkdir -p "app-store-assets/$app_name"
    cat > "app-store-assets/$app_name/app-store-listing.txt" << EOF
$display_name - App Store Listing

App Name: $display_name
Subtitle: Daily Habits & Streak Tracker
Category: Lifestyle (Primary), Health & Fitness (Secondary)
Price: Free with IAP

Description:
$icon Build lasting habits with $display_name!

Daily content delivery + streak tracking + community accountability.

Features:
• Daily habit content
• Streak tracking with milestones
• Progress analytics
• Community sharing
• Premium features available

Download $display_name today and build habits that stick!
EOF

    # Basic Marketing Plan
    mkdir -p "marketing-campaigns/social-media/$app_name"
    cat > "marketing-campaigns/social-media/$app_name/launch-plan.txt" << EOF
$display_name - Launch Marketing Plan

SOCIAL MEDIA:
- TikTok: Daily habit tips, streak celebrations
- Instagram: Progress photos, community highlights
- Twitter: Habit threads, motivation quotes

CONTENT CALENDAR:
Week 1: Launch announcement, feature highlights
Week 2: User testimonials, success stories
Week 3: Challenges, community building
Week 4: Premium promotions, advanced features

HASHTAGS: #$app_name #habittracker #streaks #consistency
EOF

    # Partnership Template
    mkdir -p "partnerships/outreach-scripts/$app_name"
    cat > "partnerships/outreach-scripts/$app_name/outreach.txt" << EOF
$display_name - Partnership Outreach

EMAIL TEMPLATE:
Subject: Free habit tracker for your community

Hi [Name],

I built $display_name to help people build daily habits with streaks.

We offer:
- Free premium access for members
- 50% discount codes
- Revenue share on upgrades

Interested in partnering?

Best,
[Your Name]
EOF

    echo "✅ $display_name launch package ready!"
}

# Create launch packages for top 10
echo "🚀 Creating LAUNCH PACKAGES for TOP 10 apps..."

for app_config in "${TOP_10_APPS[@]}"; do
    create_launch_package "$app_config"
done

echo "🎉 TOP 10 LAUNCH PACKAGES COMPLETE!"
echo "Ready for immediate App Store submission and marketing!"