#!/bin/bash

# Script to create and customize all app variants

BASE_TEMPLATE="/Users/macbookpro/Documents/app factory/app-factory/base-template/scripture-streak"

# Religious apps configuration (app_name|display_name|icon|content_type|audience|keyword|domain)
religious_apps=(
    "quran-streak|Quran Streak|🕌|quran|Islamic|Muslim|allah|quranstreak.com"
    "torah-streak|Torah Streak|✡️|torah|Jewish|Jewish|adonai|torahstreak.com"
    "gita-streak|Gita Streak|🕉️|gita|Hindu|Hindu|krishna|gitastreak.com"
    "buddhist-streak|Sutra Streak|☸️|sutra|Buddhist|Buddhist|buddha|sutrastreak.com"
    "mormon-streak|Scripture Streak|👨‍👩‍👧‍👦|scripture|Mormon|Latter-day|heavenly|mormonstreak.com"
    "sikh-streak|Guru Streak|🪯|guru|Sikh|Sikh|waheguru|gurustreak.com"
)

# Non-religious apps configuration
non_religious_apps=(
    "language-streak|Language Streak|🌍|language|Language|Learners|practice|languagestreak.com"
    "fitness-streak|Fitness Streak|💪|fitness|Fitness|Athletes|workout|fitnessstreak.com"
    "meditation-streak|Meditation Streak|🧘|meditation|Mindfulness|Practitioners|zen|meditationstreak.com"
    "reading-streak|Reading Streak|📚|reading|Reading|Book lovers|pages|readingstreak.com"
    "coding-streak|Coding Streak|💻|coding|Programming|Developers|code|codingstreak.com"
    "art-streak|Art Streak|🎨|art|Art|Artists|create|artstreak.com"
    "journal-streak|Journal Streak|📓|journal|Writing|Writers|write|journalstreak.com"
)

create_app() {
    local app_config=$1
    local category=$2

    IFS='|' read -r app_name display_name icon content_type audience keyword domain <<< "$app_config"

    echo "Creating $app_name..."

    # Copy base template
    cp -r "$BASE_TEMPLATE" "$app_name"
    cd "$app_name"

    # Fix nested structure
    if [ -d "scripture-streak" ]; then
        mv scripture-streak/* . && rmdir scripture-streak
    fi

    # Update package.json
    sed -i '' "s/scripture-streak/$app_name/g" package.json

    # Update app.json
    sed -i '' "s/Scripture Streak/$display_name/g" app.json
    sed -i '' "s/scripture-streak/$app_name/g" app.json
    sed -i '' "s/com.fnsmdehip.scripture-streak/com.fnsmdehip.$app_name/g" app.json

    # Update README
    sed -i '' "s/Scripture Streak /$display_name /g" README.md
    sed -i '' "s/📖🔥/📖$icon/g" README.md
    sed -i '' "s/Bible reading/$content_type reading/g" README.md
    sed -i '' "s/scripturestreak.com/$domain/g" README.md

    # Update app store listing
    sed -i '' "s/Scripture Streak - Bible Habits/$display_name - $content_type Habits/g" docs/APP-STORE-LISTING.md
    sed -i '' "s/scripturestreak.com/$domain/g" docs/APP-STORE-LISTING.md

    cd ..
    echo "$app_name created successfully"
}

# Create religious apps
mkdir -p religious-apps
cd religious-apps

for app_config in "${religious_apps[@]}"; do
    create_app "$app_config" "religious"
done

cd ..

# Create non-religious apps
mkdir -p non-religious-apps
cd non-religious-apps

for app_config in "${non_religious_apps[@]}"; do
    create_app "$app_config" "non-religious"
done

cd ..

echo "All apps created successfully!"