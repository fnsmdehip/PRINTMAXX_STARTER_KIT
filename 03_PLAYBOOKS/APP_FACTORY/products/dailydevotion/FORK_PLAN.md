# DailyDevotion Fork Plan

**Source:** Loop Habit Tracker (github.com/iSoron/uhabits)
**License:** MIT (commercial use permitted)
**Target Niche:** Faith/Christian habit tracking
**Mascot:** Dove (peace, Holy Spirit symbolism)

---

## Original App Analysis

### Loop Habit Tracker Overview
- **Language:** Kotlin (Android native)
- **Architecture:** Clean Architecture with MVVM
- **Database:** SQLite with Room
- **Charts:** Custom canvas-based visualizations
- **License:** MIT (permissive, commercial OK)
- **Stars:** 7000+ on GitHub
- **Last Updated:** Actively maintained

### Key Directories (uhabits repo)

```
uhabits/
├── uhabits-android/          # Main Android app module
│   ├── src/main/
│   │   ├── java/org/isoron/uhabits/
│   │   │   ├── activities/     # UI Activities
│   │   │   ├── automation/     # Tasker integration
│   │   │   ├── core/           # Business logic
│   │   │   ├── inject/         # Dependency injection
│   │   │   ├── intents/        # Intent handlers
│   │   │   ├── notifications/  # Notification system
│   │   │   ├── preferences/    # Settings
│   │   │   ├── receivers/      # Broadcast receivers
│   │   │   ├── sync/           # Sync functionality
│   │   │   ├── utils/          # Utility classes
│   │   │   └── widgets/        # Home screen widgets
│   │   └── res/
│   │       ├── drawable/       # Icons, shapes
│   │       ├── layout/         # XML layouts
│   │       ├── values/         # Colors, strings, themes
│   │       └── raw/            # Sound files
│   └── build.gradle.kts
├── uhabits-core/             # Shared business logic
│   └── src/main/java/org/isoron/uhabits/core/
│       ├── commands/           # Command pattern
│       ├── database/           # Database operations
│       ├── io/                 # Import/export
│       ├── models/             # Data models
│       ├── preferences/        # Core preferences
│       ├── reminders/          # Reminder logic
│       ├── tasks/              # Background tasks
│       └── utils/              # Core utilities
├── uhabits-server/           # Optional sync server
└── build.gradle.kts
```

### Core Features in Original
1. Boolean habits (done/not done)
2. Numeric habits (track quantities)
3. Flexible schedules (daily, weekly, custom)
4. Streak tracking with visualizations
5. Charts (frequency, history, calendar)
6. Reminders and notifications
7. Widgets (checkmark, frequency, history)
8. Data export/backup
9. Dark mode
10. Material Design UI

---

## Modifications for DailyDevotion

### 1. Branding Changes

#### App Identity
| Original | DailyDevotion |
|----------|---------------|
| Loop Habit Tracker | DailyDevotion |
| org.isoron.uhabits | com.dailydevotion.app |
| Green accent color | Soft purple/gold |
| Checkmark logo | Dove mascot |

#### Files to Modify
```
# Package rename
- All Java/Kotlin files: org.isoron.uhabits -> com.dailydevotion.app
- AndroidManifest.xml: package name
- build.gradle: applicationId

# App name strings
- res/values/strings.xml: app_name
- res/values-*/strings.xml: translations

# Icons
- res/mipmap-*/ic_launcher.png: Replace with dove icon
- res/drawable/ic_launcher_foreground.xml: New dove vector
```

---

### 2. Color Scheme Changes

#### Original Colors (Green-focused)
```xml
<!-- Original Loop colors -->
<color name="colorPrimary">#303F9F</color>
<color name="colorAccent">#4CAF50</color>
```

#### DailyDevotion Colors (Spiritual palette)
```xml
<!-- Faith-focused calming palette -->
<color name="colorPrimary">#5E4B8B</color>      <!-- Deep purple (royalty, spirituality) -->
<color name="colorPrimaryDark">#3E2C5B</color>  <!-- Darker purple -->
<color name="colorAccent">#D4AF37</color>       <!-- Gold (divinity, glory) -->
<color name="colorBackground">#F8F6FA</color>   <!-- Soft lavender white -->
<color name="colorSurface">#FFFFFF</color>
<color name="colorOnPrimary">#FFFFFF</color>
<color name="colorSecondary">#7B9E89</color>    <!-- Sage green (peace, growth) -->

<!-- Habit completion colors -->
<color name="colorStreakGold">#D4AF37</color>
<color name="colorPrayerPurple">#8B7BB5</color>
<color name="colorScriptureBlue">#5B7C99</color>
<color name="colorGratitudeGreen">#7B9E89</color>
```

#### Files to Modify
```
- res/values/colors.xml
- res/values-night/colors.xml (dark mode)
- res/values/themes.xml
```

---

### 3. Faith-Specific Habit Templates

#### Pre-built Templates to Add
```kotlin
// New file: core/templates/FaithTemplates.kt

object FaithTemplates {

    val MORNING_PRAYER = HabitTemplate(
        name = "Morning Prayer",
        description = "Start your day with God",
        icon = R.drawable.ic_prayer_hands,
        color = Color.PRAYER_PURPLE,
        frequency = Frequency.DAILY,
        targetType = HabitType.BOOLEAN,
        reminderTime = "06:00"
    )

    val SCRIPTURE_READING = HabitTemplate(
        name = "Scripture Reading",
        description = "Read God's Word daily",
        icon = R.drawable.ic_bible,
        color = Color.SCRIPTURE_BLUE,
        frequency = Frequency.DAILY,
        targetType = HabitType.NUMERIC,
        targetValue = 15, // minutes
        unit = "minutes"
    )

    val GRATITUDE_JOURNAL = HabitTemplate(
        name = "Gratitude Journal",
        description = "Count your blessings",
        icon = R.drawable.ic_journal,
        color = Color.GRATITUDE_GREEN,
        frequency = Frequency.DAILY,
        targetType = HabitType.NUMERIC,
        targetValue = 3, // items
        unit = "things"
    )

    val CHURCH_ATTENDANCE = HabitTemplate(
        name = "Church Attendance",
        description = "Gather with believers",
        icon = R.drawable.ic_church,
        color = Color.PRIMARY,
        frequency = Frequency.WEEKLY,
        targetType = HabitType.BOOLEAN
    )

    val SABBATH_REST = HabitTemplate(
        name = "Sabbath Rest",
        description = "Honor the Lord's day",
        icon = R.drawable.ic_sabbath,
        color = Color.ACCENT,
        frequency = Frequency.WEEKLY,
        targetType = HabitType.BOOLEAN
    )

    val FASTING = HabitTemplate(
        name = "Fasting",
        description = "Spiritual discipline",
        icon = R.drawable.ic_fasting,
        color = Color.SECONDARY,
        frequency = Frequency.CUSTOM,
        targetType = HabitType.BOOLEAN
    )

    val TITHE_GIVING = HabitTemplate(
        name = "Tithe/Giving",
        description = "Give generously",
        icon = R.drawable.ic_giving,
        color = Color.STREAK_GOLD,
        frequency = Frequency.WEEKLY,
        targetType = HabitType.BOOLEAN
    )

    val EVENING_PRAYER = HabitTemplate(
        name = "Evening Prayer",
        description = "End your day with God",
        icon = R.drawable.ic_moon_prayer,
        color = Color.PRIMARY_DARK,
        frequency = Frequency.DAILY,
        targetType = HabitType.BOOLEAN,
        reminderTime = "21:00"
    )

    val MEDITATION = HabitTemplate(
        name = "Christian Meditation",
        description = "Be still and know",
        icon = R.drawable.ic_meditation,
        color = Color.PRAYER_PURPLE,
        frequency = Frequency.DAILY,
        targetType = HabitType.NUMERIC,
        targetValue = 10,
        unit = "minutes"
    )

    val SCRIPTURE_MEMORIZATION = HabitTemplate(
        name = "Scripture Memorization",
        description = "Hide God's Word in your heart",
        icon = R.drawable.ic_memory,
        color = Color.SCRIPTURE_BLUE,
        frequency = Frequency.WEEKLY,
        targetType = HabitType.NUMERIC,
        targetValue = 1,
        unit = "verses"
    )

    // All templates list
    val ALL = listOf(
        MORNING_PRAYER,
        SCRIPTURE_READING,
        GRATITUDE_JOURNAL,
        CHURCH_ATTENDANCE,
        EVENING_PRAYER,
        MEDITATION,
        FASTING,
        TITHE_GIVING,
        SABBATH_REST,
        SCRIPTURE_MEMORIZATION
    )
}
```

#### Files to Create/Modify
```
# New files
- core/templates/FaithTemplates.kt
- core/templates/HabitTemplate.kt
- activities/habits/create/TemplatePickerActivity.kt

# Modify
- activities/habits/create/CreateHabitActivity.kt (add template selection)
- res/layout/activity_create_habit.xml (add template button)
```

---

### 4. New Feature: Bible Verse of the Day

#### API Integration
```kotlin
// New file: core/verse/VerseOfDayService.kt

interface BibleApiService {
    @GET("verse/random")
    suspend fun getRandomVerse(): VerseResponse

    @GET("verse/{reference}")
    suspend fun getVerse(@Path("reference") reference: String): VerseResponse
}

data class VerseResponse(
    val reference: String,      // "John 3:16"
    val text: String,           // "For God so loved..."
    val translation: String     // "NIV"
)

class VerseOfDayService(
    private val api: BibleApiService,
    private val prefs: SharedPreferences
) {
    suspend fun getTodayVerse(): VerseResponse {
        val cached = getCachedVerse()
        if (cached != null && isCacheFresh()) {
            return cached
        }

        val verse = api.getRandomVerse()
        cacheVerse(verse)
        return verse
    }
}
```

#### API Options (Free)
1. **bible-api.com** - Public domain translations (KJV, WEB)
2. **labs.bible.org** - NET Bible API
3. **api.scripture.api.bible** - Multiple translations (requires key)

#### UI Components
```xml
<!-- New file: res/layout/card_verse_of_day.xml -->
<androidx.cardview.widget.CardView
    android:layout_width="match_parent"
    android:layout_height="wrap_content"
    app:cardCornerRadius="16dp"
    app:cardElevation="4dp">

    <LinearLayout
        android:orientation="vertical"
        android:padding="16dp">

        <ImageView
            android:src="@drawable/ic_dove"
            android:layout_gravity="center"/>

        <TextView
            android:id="@+id/verseText"
            android:textStyle="italic"
            android:textSize="16sp"/>

        <TextView
            android:id="@+id/verseReference"
            android:textStyle="bold"
            android:textSize="14sp"/>

        <Button
            android:id="@+id/shareButton"
            android:text="Share"
            style="@style/Widget.MaterialComponents.Button.TextButton"/>
    </LinearLayout>
</androidx.cardview.widget.CardView>
```

#### Files to Create
```
# New files
- core/verse/VerseOfDayService.kt
- core/verse/BibleApiService.kt
- core/verse/VerseRepository.kt
- activities/verse/VerseOfDayFragment.kt
- res/layout/card_verse_of_day.xml
- res/layout/fragment_verse_of_day.xml
```

---

### 5. Dove Mascot Implementation

#### Required Assets
```
# App icons (all sizes)
res/mipmap-mdpi/ic_launcher.png      (48x48)
res/mipmap-hdpi/ic_launcher.png      (72x72)
res/mipmap-xhdpi/ic_launcher.png     (96x96)
res/mipmap-xxhdpi/ic_launcher.png    (144x144)
res/mipmap-xxxhdpi/ic_launcher.png   (192x192)

# Adaptive icon components
res/drawable/ic_launcher_foreground.xml   (dove vector)
res/drawable/ic_launcher_background.xml   (gradient)

# In-app mascot appearances
res/drawable/dove_greeting.xml        (welcome screen)
res/drawable/dove_celebrating.xml     (streak achievement)
res/drawable/dove_encouraging.xml     (missed habit)
res/drawable/dove_praying.xml         (prayer habit complete)
```

#### Mascot Personality Messages
```kotlin
// New file: core/mascot/DoveMascot.kt

object DoveMascot {

    val GREETINGS = listOf(
        "Peace be with you today!",
        "Ready to grow in faith?",
        "Let's walk together in the Spirit.",
        "God's grace is new every morning!"
    )

    val STREAK_CELEBRATIONS = mapOf(
        7 to "One week of faithfulness! Keep pressing on!",
        30 to "A month of devotion! You're building holy habits!",
        100 to "100 days! Your dedication inspires!",
        365 to "One year! What an incredible journey of faith!"
    )

    val ENCOURAGEMENTS = listOf(
        "His mercies are new every morning.",
        "Don't give up - you're growing!",
        "Tomorrow is a new opportunity.",
        "Grace covers yesterday. Let's focus on today."
    )

    val COMPLETION_MESSAGES = listOf(
        "Well done, faithful servant!",
        "You've honored God today.",
        "Another step in your spiritual journey!",
        "Heaven rejoices with you!"
    )
}
```

---

### 6. UI Modifications

#### Splash Screen
```xml
<!-- res/layout/activity_splash.xml -->
<ConstraintLayout>
    <ImageView
        android:id="@+id/doveLogo"
        android:src="@drawable/dove_large"/>

    <TextView
        android:text="DailyDevotion"
        android:textSize="32sp"
        android:fontFamily="@font/serif"/>

    <TextView
        android:text="Grow in faith, one habit at a time"
        android:textSize="16sp"/>
</ConstraintLayout>
```

#### Custom Fonts
```
res/font/
├── lora_regular.ttf       # Elegant serif for headings
├── lora_italic.ttf        # For verse display
├── source_sans_regular.ttf # Clean sans for body
└── source_sans_bold.ttf
```

#### Modified Strings
```xml
<!-- res/values/strings.xml -->
<resources>
    <string name="app_name">DailyDevotion</string>
    <string name="tagline">Grow in faith, one habit at a time</string>

    <!-- Renamed from generic to faith-focused -->
    <string name="streak_label">Faithfulness Streak</string>
    <string name="completion_rate">Growth Rate</string>
    <string name="habits_title">Spiritual Disciplines</string>
    <string name="add_habit">Add Discipline</string>

    <!-- New faith strings -->
    <string name="verse_of_day">Today\'s Scripture</string>
    <string name="share_verse">Share Blessing</string>
    <string name="prayer_reminder">Time for Prayer</string>
    <string name="missed_habit_grace">Grace covers yesterday</string>
</resources>
```

---

### 7. Notification Modifications

#### Faith-Themed Reminders
```kotlin
// Modify: notifications/ReminderNotificationBuilder.kt

class FaithReminderBuilder {

    fun buildPrayerReminder(habit: Habit): Notification {
        return NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_dove_small)
            .setContentTitle("Time for ${habit.name}")
            .setContentText(getEncouragingMessage(habit))
            .setStyle(NotificationCompat.BigTextStyle()
                .bigText("${getVerseSnippet()}\n\n${habit.description}"))
            .build()
    }

    private fun getEncouragingMessage(habit: Habit): String {
        return when (habit.type) {
            HabitType.PRAYER -> "Come boldly to the throne of grace"
            HabitType.SCRIPTURE -> "Thy word is a lamp unto my feet"
            HabitType.GRATITUDE -> "Give thanks in all circumstances"
            else -> "Be faithful in this small thing"
        }
    }
}
```

---

### 8. Widget Modifications

#### DailyDevotion Widget
```xml
<!-- res/layout/widget_devotion.xml -->
<LinearLayout
    android:background="@drawable/widget_background_gold">

    <ImageView
        android:src="@drawable/ic_dove_small"/>

    <TextView
        android:id="@+id/verseSnippet"
        android:maxLines="2"/>

    <LinearLayout android:orientation="horizontal">
        <!-- Quick habit checkboxes -->
        <CheckBox android:id="@+id/prayerCheck"/>
        <CheckBox android:id="@+id/scriptureCheck"/>
        <CheckBox android:id="@+id/gratitudeCheck"/>
    </LinearLayout>

    <TextView
        android:id="@+id/streakCount"
        android:text="7 day streak"/>
</LinearLayout>
```

---

## Implementation Phases

### Phase 1: Core Branding (Day 1-2)
- [ ] Fork repository
- [ ] Rename package to com.dailydevotion.app
- [ ] Update app name and strings
- [ ] Replace color scheme
- [ ] Create/integrate dove icon

### Phase 2: Faith Templates (Day 2-3)
- [ ] Create HabitTemplate data class
- [ ] Implement FaithTemplates object
- [ ] Add template picker UI
- [ ] Wire templates to habit creation

### Phase 3: Verse of Day (Day 3-4)
- [ ] Integrate Bible API
- [ ] Create VerseOfDayService
- [ ] Build verse card UI
- [ ] Add to main screen
- [ ] Implement caching

### Phase 4: Mascot & Polish (Day 4-5)
- [ ] Create dove mascot assets (or commission)
- [ ] Implement mascot messages
- [ ] Add celebration animations
- [ ] Custom fonts
- [ ] Splash screen

### Phase 5: Widget & Notifications (Day 5-6)
- [ ] Faith-themed notifications
- [ ] Verse-in-notification option
- [ ] DailyDevotion widget
- [ ] Quick-complete from widget

### Phase 6: Testing & Launch Prep (Day 6-7)
- [ ] Full functional testing
- [ ] Performance testing
- [ ] Store screenshots
- [ ] Store description
- [ ] Privacy policy
- [ ] Beta test with 10+ users

---

## Files Summary

### Files to Modify (from original)
```
uhabits-android/
├── build.gradle.kts                    # Package name, deps
├── src/main/AndroidManifest.xml        # Package, permissions
├── src/main/res/
│   ├── values/strings.xml              # All user-facing text
│   ├── values/colors.xml               # Color palette
│   ├── values/themes.xml               # Theme definitions
│   ├── values-night/colors.xml         # Dark mode
│   ├── mipmap-*/ic_launcher.png        # App icons
│   └── drawable/ic_launcher_*.xml      # Adaptive icons
└── src/main/java/org/isoron/uhabits/
    ├── HabitsApplication.kt            # App initialization
    ├── activities/habits/list/         # Main list view
    └── notifications/                  # Notification builders
```

### New Files to Create
```
uhabits-android/src/main/
├── java/com/dailydevotion/app/
│   ├── core/
│   │   ├── templates/
│   │   │   ├── HabitTemplate.kt
│   │   │   └── FaithTemplates.kt
│   │   ├── verse/
│   │   │   ├── BibleApiService.kt
│   │   │   ├── VerseOfDayService.kt
│   │   │   └── VerseRepository.kt
│   │   └── mascot/
│   │       └── DoveMascot.kt
│   ├── activities/
│   │   ├── templates/
│   │   │   └── TemplatePickerActivity.kt
│   │   └── verse/
│   │       └── VerseOfDayFragment.kt
│   └── widgets/
│       └── DevotionWidget.kt
└── res/
    ├── layout/
    │   ├── card_verse_of_day.xml
    │   ├── activity_template_picker.xml
    │   ├── item_template.xml
    │   └── widget_devotion.xml
    ├── drawable/
    │   ├── dove_greeting.xml
    │   ├── dove_celebrating.xml
    │   ├── ic_prayer_hands.xml
    │   ├── ic_bible.xml
    │   ├── ic_journal.xml
    │   ├── ic_church.xml
    │   └── [other faith icons]
    └── font/
        ├── lora_regular.ttf
        └── source_sans_regular.ttf
```

### New Assets Needed
```
assets/
├── icons/
│   ├── dove_app_icon.svg          # Main app icon
│   ├── dove_greeting.svg          # Mascot variants
│   ├── dove_celebrating.svg
│   ├── dove_encouraging.svg
│   ├── ic_prayer_hands.svg        # Habit icons
│   ├── ic_bible.svg
│   ├── ic_journal.svg
│   ├── ic_church.svg
│   ├── ic_fasting.svg
│   ├── ic_giving.svg
│   └── ic_meditation.svg
├── store/
│   ├── feature_graphic.png        # 1024x500
│   ├── screenshot_1.png           # Phone screenshots
│   ├── screenshot_2.png
│   ├── screenshot_3.png
│   └── promo_video.mp4            # Optional
└── marketing/
    ├── social_banner.png
    └── icon_variants/             # Different contexts
```

---

## Dependencies to Add

```kotlin
// build.gradle.kts additions

dependencies {
    // Bible API
    implementation("com.squareup.retrofit2:retrofit:2.9.0")
    implementation("com.squareup.retrofit2:converter-gson:2.9.0")

    // Custom fonts
    implementation("androidx.core:core-ktx:1.12.0")

    // Animations for mascot
    implementation("com.airbnb.android:lottie:6.1.0")
}
```

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Bible API rate limits | Cache aggressively, fallback to local verses |
| Kotlin version mismatch | Match original repo's Kotlin version exactly |
| Breaking original features | Fork cleanly, test thoroughly before adding |
| Asset creation delays | Use placeholder icons, commission dove ASAP |
| Play Store rejection | Review policy, add proper disclaimers |

---

## Success Metrics

| Metric | Target |
|--------|--------|
| Fork to first build | < 4 hours |
| All branding changes | < 8 hours |
| Faith templates working | < 4 hours |
| Verse API integrated | < 6 hours |
| Store-ready | < 1 week |

---

## License Compliance

The MIT License requires:
1. Include original copyright notice
2. Include license text in distribution

Add to app settings/about screen:
```
DailyDevotion is built on Loop Habit Tracker
Copyright (c) 2016-2024 Alison Bento and contributors
Licensed under MIT License
```

---

Created: 2026-01-21
Status: PLANNING
