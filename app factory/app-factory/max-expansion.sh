#!/bin/bash

# MAXIMUM EXPANSION SCRIPT - Create ALL the apps and campaigns

BASE_TEMPLATE="/Users/macbookpro/Documents/app factory/app-factory/base-template/scripture-streak"

# EXTENDED RELIGIOUS APPS
extended_religious_apps=(
    "catholic-streak|Catholic Streak|⛪|catholic|Catholic|jesus|catholicstreak.com"
    "orthodox-streak|Orthodox Streak|☦️|orthodox|Orthodox|christ|orthodoxstreak.com"
    "protestant-streak|Protestant Streak|⛪|protestant|Protestant|grace|protestantstreak.com"
    "baptist-streak|Baptist Streak|⛪|baptist|Baptist|baptism|baptiststreak.com"
    "methodist-streak|Methodist Streak|⛪|methodist|Methodist|worship|methodiststreak.com"
    "lutheran-streak|Lutheran Streak|⛪|lutheran|Lutheran|faith|lutheranstreak.com"
    "episcopal-streak|Episcopal Streak|⛪|episcopal|Episcopal|prayer|episcopalstreak.com"
    "pentecostal-streak|Pentecostal Streak|⛪|pentecostal|Pentecostal|spirit|pentecostalstreak.com"
    "evangelical-streak|Evangelical Streak|⛪|evangelical|Evangelical|gospel|evangelicalstreak.com"
    "anglican-streak|Anglican Streak|⛪|anglican|Anglican|tradition|anglicanstreak.com"
    "presbyterian-streak|Presbyterian Streak|⛪|presbyterian|Presbyterian|covenant|presbyterianstreak.com"
    "shia-streak|Shia Streak|🕌|shia|Shia|imam|shiaquranstreak.com"
    "sunni-streak|Sunni Streak|🕌|sunni|Sunni|prophet|sunniquranstreak.com"
    "sufi-streak|Sufi Streak|🕌|sufi|Sufi|mystic|sufistreak.com"
    "hindu-vedas-streak|Vedas Streak|🕉️|vedas|Vedic|sanskrit|vedasstreak.com"
    "hindu-upanishads-streak|Upanishads Streak|🕉️|upanishads|Vedantic|consciousness|upanishadsstreak.com"
    "hindu-mahabharata-streak|Mahabharata Streak|🕉️|mahabharata|Epic|dharma|mahabharatastreak.com"
    "jain-streak|Jain Streak|☸️|jain|Jain|ahimsa|jainstreak.com"
    "taoist-streak|Taoist Streak|☯️|taoist|Taoist|harmony|taoiststreak.com"
    "confucian-streak|Confucian Streak|📚|confucian|Confucian|virtue|confucianstreak.com"
    "shinto-streak|Shinto Streak|⛩️|shinto|Shinto|kami|shintostreak.com"
    "zoroastrian-streak|Zoroastrian Streak|🔥|zoroastrian|Zoroastrian|fire|zoroastrianstreak.com"
    "bahai-streak|Bahai Streak|🌍|bahai|Bahai|unity|bahaiwritingsstreak.com"
    "sikh-guru-streak|Sikh Guru Streak|🪯|sikh-guru|Sikh|truth|gurusikhstreak.com"
    "rastafarian-streak|Rastafarian Streak|🦁|rastafarian|Rasta|jah|rastastreak.com"
)

# EDUCATION APPS
education_apps=(
    "spanish-streak|Spanish Streak|🇪🇸|spanish|Spanish|hablo|spanishstreak.com"
    "french-streak|French Streak|🇫🇷|french|French|parle|frenchstreak.com"
    "german-streak|German Streak|🇩🇪|german|German|spreche|germanstreak.com"
    "italian-streak|Italian Streak|🇮🇹|italian|Italian|parlo|italianstreak.com"
    "japanese-streak|Japanese Streak|🇯🇵|japanese|Japanese|hanasu|japanesestreak.com"
    "chinese-streak|Chinese Streak|🇨🇳|chinese|Mandarin|shuochina|chinesestreak.com"
    "korean-streak|Korean Streak|🇰🇷|korean|Korean|malhae|koreanstreak.com"
    "arabic-streak|Arabic Streak|🇸🇦|arabic|Arabic|atakallam|arabicstreak.com"
    "russian-streak|Russian Streak|🇷🇺|russian|Russian|govoryu|russianstreak.com"
    "portuguese-streak|Portuguese Streak|🇧🇷|portuguese|Portuguese|falo|portuguesestreak.com"
    "hindi-streak|Hindi Streak|🇮🇳|hindi|Hindi|bolta|hindiindianstreak.com"
    "math-streak|Math Streak|🔢|math|Mathematics|calculate|mathstreak.com"
    "physics-streak|Physics Streak|⚛️|physics|Physics|einstein|physicsstreak.com"
    "chemistry-streak|Chemistry Streak|🧪|chemistry|Chemistry|molecule|chemistrystreak.com"
    "biology-streak|Biology Streak|🧬|biology|Biology|darwin|biologystreak.com"
    "history-streak|History Streak|📜|history|History|learn|historystreak.com"
    "geography-streak|Geography Streak|🌍|geography|Geography|explore|geographystreak.com"
    "music-theory-streak|Music Theory Streak|🎼|music-theory|Music Theory|compose|musictheorystreak.com"
    "guitar-streak|Guitar Streak|🎸|guitar|Guitar|play|guitarstreak.com"
    "piano-streak|Piano Streak|🎹|piano|Piano|play|pianostreak.com"
)

# HEALTH & WELLNESS APPS
health_apps=(
    "running-streak|Running Streak|🏃|running|Running|marathon|runningstreak.com"
    "weightlifting-streak|Weightlifting Streak|🏋️|weightlifting|Weightlifting|lifting|weightliftingstreak.com"
    "yoga-streak|Yoga Streak|🧘‍♀️|yoga|Yoga|namaste|yogastreak.com"
    "pilates-streak|Pilates Streak|🤸‍♀️|pilates|Pilates|core|pilatessstreak.com"
    "cardio-streak|Cardio Streak|❤️|cardio|Cardio|heart|cardiostreak.com"
    "swimming-streak|Swimming Streak|🏊|swimming|Swimming|stroke|swimmingstreak.com"
    "cycling-streak|Cycling Streak|🚴|cycling|Cycling|pedal|cyclingstreak.com"
    "walking-streak|Walking Streak|🚶|walking|Walking|steps|walkingstreak.com"
    "nutrition-streak|Nutrition Streak|🥗|nutrition|Nutrition|healthy|nutritionstreak.com"
    "intermittent-fasting-streak|Intermittent Fasting|⏰|fasting|Fasting|fast|fastingstreak.com"
    "keto-streak|Keto Streak|🥑|keto|Ketogenic|keto|ketostreak.com"
    "vegan-streak|Vegan Streak|🌱|vegan|Vegan|plant|veganstreak.com"
    "mindfulness-streak|Mindfulness Streak|🧠|mindfulness|Mindfulness|present|mindfulnessstreak.com"
    "breathing-streak|Breathing Streak|🌬️|breathing|Breathing|breathe|breathingstreak.com"
    "sleep-streak|Sleep Streak|😴|sleep|Sleep|rest|sleepstreak.com"
    "stress-relief-streak|Stress Relief Streak|😌|stress-relief|Stress Relief|calm|stressreliefstreak.com"
    "gratitude-streak|Gratitude Streak|🙏|gratitude|Gratitude|thankful|gratitudestreak.com"
    "positive-affirmations-streak|Positive Affirmations|✨|affirmations|Affirmations|positive|affirmationsstreak.com"
)

# PERSONAL GROWTH APPS
personal_growth_apps=(
    "goal-setting-streak|Goal Setting Streak|🎯|goals|Goals|achieve|goalstreak.com"
    "productivity-streak|Productivity Streak|⚡|productivity|Productivity|focus|productivitystreak.com"
    "time-management-streak|Time Management|⏰|time-management|Time Management|organize|timemanagementstreak.com"
    "public-speaking-streak|Public Speaking|🎤|public-speaking|Public Speaking|speak|publicspeakingstreak.com"
    "confidence-streak|Confidence Streak|💪|confidence|Confidence|believe|confidencestreak.com"
    "leadership-streak|Leadership Streak|👑|leadership|Leadership|lead|leadershipstreak.com"
    "networking-streak|Networking Streak|🤝|networking|Networking|connect|networkingstreak.com"
    "sales-streak|Sales Streak|💰|sales|Sales|close|salesstreak.com"
    "negotiation-streak|Negotiation Streak|⚖️|negotiation|Negotiation|deal|negotiationstreak.com"
    "critical-thinking-streak|Critical Thinking|🧠|critical-thinking|Critical Thinking|think|criticalthinkingstreak.com"
    "problem-solving-streak|Problem Solving|🛠️|problem-solving|Problem Solving|solve|problemsolvingstreak.com"
    "decision-making-streak|Decision Making|🎲|decision-making|Decision Making|choose|decisionmakingstreak.com"
)

# PROFESSIONAL APPS
professional_apps=(
    "project-management-streak|Project Management|📋|project-management|Project Management|manage|projectmanagementstreak.com"
    "agile-streak|Agile Streak|🔄|agile|Agile|iterate|agilestreak.com"
    "scrum-streak|Scrum Streak|🏉|scrum|Scrum|sprint|scrumstreak.com"
    "kanban-streak|Kanban Streak|📊|kanban|Kanban|flow|kanbanstreak.com"
    "data-analysis-streak|Data Analysis|📈|data-analysis|Data Analysis|analyze|dataanalysisstreak.com"
    "machine-learning-streak|Machine Learning|🤖|machine-learning|Machine Learning|learn|machinelearningstreak.com"
    "ux-design-streak|UX Design Streak|🎨|ux-design|UX Design|design|uxdesignstreak.com"
    "ui-design-streak|UI Design Streak|💻|ui-design|UI Design|interface|uidesignstreak.com"
    "web-development-streak|Web Development|🌐|web-development|Web Development|code|webdevstreak.com"
    "mobile-development-streak|Mobile Development|📱|mobile-development|Mobile Development|app|mobiledevstreak.com"
    "devops-streak|DevOps Streak|⚙️|devops|DevOps|deploy|devopsstreak.com"
    "cloud-computing-streak|Cloud Computing|☁️|cloud-computing|Cloud Computing|scale|cloudstreak.com"
)

create_app() {
    local app_config=$1
    local category=$2

    IFS='|' read -r app_name display_name icon content_type audience keyword domain <<< "$app_config"

    echo "Creating $app_name in $category..."

    # Create category directory if it doesn't exist
    mkdir -p "$category"

    # Copy base template
    cp -r "$BASE_TEMPLATE" "$category/$app_name"
    cd "$category/$app_name"

    # Fix nested structure
    if [ -d "scripture-streak" ]; then
        mv scripture-streak/* . && rmdir scripture-streak 2>/dev/null
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

    # Create marketing campaign files
    mkdir -p "../../marketing-campaigns/social-media/$app_name"
    mkdir -p "../../marketing-campaigns/ad-campaigns/$app_name"
    mkdir -p "../../marketing-campaigns/email-sequences/$app_name"
    mkdir -p "../../app-store-assets/screenshots/$app_name"
    mkdir -p "../../app-store-assets/icons/$app_name"
    mkdir -p "../../partnerships/outreach-scripts/$app_name"

    cd ../..
    echo "$app_name created successfully"
}

# Create ALL the apps
echo "Starting MASSIVE app creation..."

# Extended Religious Apps
echo "Creating Extended Religious Apps..."
for app_config in "${extended_religious_apps[@]}"; do
    create_app "$app_config" "expanded-apps/religious-extended"
done

# Education Apps
echo "Creating Education Apps..."
for app_config in "${education_apps[@]}"; do
    create_app "$app_config" "expanded-apps/education"
done

# Health & Wellness Apps
echo "Creating Health & Wellness Apps..."
for app_config in "${health_apps[@]}"; do
    create_app "$app_config" "expanded-apps/health-wellness"
done

# Personal Growth Apps
echo "Creating Personal Growth Apps..."
for app_config in "${personal_growth_apps[@]}"; do
    create_app "$app_config" "expanded-apps/personal-growth"
done

# Professional Apps
echo "Creating Professional Apps..."
for app_config in "${professional_apps[@]}"; do
    create_app "$app_config" "expanded-apps/professional"
done

echo "MASSIVE EXPANSION COMPLETE!"
echo "Created $((${#extended_religious_apps[@]} + ${#education_apps[@]} + ${#health_apps[@]} + ${#personal_growth_apps[@]} + ${#professional_apps[@]})) additional apps!"
echo "Total apps in factory: $((${#extended_religious_apps[@]} + ${#education_apps[@]} + ${#health_apps[@]} + ${#personal_growth_apps[@]} + ${#professional_apps[@]} + 13))"