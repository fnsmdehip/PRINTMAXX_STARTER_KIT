package com.dailydevotion.app.core.templates

import com.dailydevotion.app.R
import com.dailydevotion.app.core.models.DisciplineCategory
import com.dailydevotion.app.core.models.Frequency
import com.dailydevotion.app.core.models.HabitType

/**
 * Pre-built faith habit templates.
 *
 * These templates cover the core spiritual disciplines commonly practiced
 * by Christians. Each template has sensible defaults for frequency, targets,
 * and reminder times based on typical practice patterns.
 */
object FaithTemplates {

    // ===================
    // PRAYER TEMPLATES
    // ===================

    val MORNING_PRAYER = HabitTemplate(
        id = "morning_prayer",
        name = "Morning Prayer",
        description = "Start your day in conversation with God",
        category = DisciplineCategory.PRAYER,
        iconRes = R.drawable.ic_prayer_hands,
        colorRes = R.color.prayer_purple,
        frequency = Frequency.DAILY,
        targetType = HabitType.BOOLEAN,
        reminderTime = "06:00",
        verseReference = "Psalm 5:3"  // "In the morning, Lord, you hear my voice"
    )

    val EVENING_PRAYER = HabitTemplate(
        id = "evening_prayer",
        name = "Evening Prayer",
        description = "End your day giving thanks and seeking rest",
        category = DisciplineCategory.PRAYER,
        iconRes = R.drawable.ic_moon_prayer,
        colorRes = R.color.prayer_purple_dark,
        frequency = Frequency.DAILY,
        targetType = HabitType.BOOLEAN,
        reminderTime = "21:00",
        verseReference = "Psalm 4:8"  // "In peace I will lie down and sleep"
    )

    val CHRISTIAN_MEDITATION = HabitTemplate(
        id = "meditation",
        name = "Christian Meditation",
        description = "Be still and know that He is God",
        category = DisciplineCategory.PRAYER,
        iconRes = R.drawable.ic_meditation,
        colorRes = R.color.prayer_purple_light,
        frequency = Frequency.DAILY,
        targetType = HabitType.NUMERIC,
        targetValue = 10,
        unit = "minutes",
        reminderTime = "07:00",
        verseReference = "Psalm 46:10"  // "Be still, and know that I am God"
    )

    val GRATITUDE_JOURNAL = HabitTemplate(
        id = "gratitude_journal",
        name = "Gratitude Journal",
        description = "Count your blessings and give thanks",
        category = DisciplineCategory.PRAYER,
        iconRes = R.drawable.ic_journal,
        colorRes = R.color.gratitude_green,
        frequency = Frequency.DAILY,
        targetType = HabitType.NUMERIC,
        targetValue = 3,
        unit = "things",
        verseReference = "1 Thessalonians 5:18"  // "Give thanks in all circumstances"
    )

    // ===================
    // SCRIPTURE TEMPLATES
    // ===================

    val SCRIPTURE_READING = HabitTemplate(
        id = "scripture_reading",
        name = "Scripture Reading",
        description = "Daily time in God's Word",
        category = DisciplineCategory.SCRIPTURE,
        iconRes = R.drawable.ic_bible,
        colorRes = R.color.scripture_blue,
        frequency = Frequency.DAILY,
        targetType = HabitType.NUMERIC,
        targetValue = 15,
        unit = "minutes",
        reminderTime = "06:30",
        verseReference = "Psalm 119:105"  // "Your word is a lamp for my feet"
    )

    val SCRIPTURE_MEMORIZATION = HabitTemplate(
        id = "scripture_memory",
        name = "Scripture Memorization",
        description = "Hide God's Word in your heart",
        category = DisciplineCategory.SCRIPTURE,
        iconRes = R.drawable.ic_memory,
        colorRes = R.color.scripture_blue_dark,
        frequency = Frequency.WEEKLY,
        targetType = HabitType.NUMERIC,
        targetValue = 1,
        unit = "verses",
        verseReference = "Psalm 119:11"  // "I have hidden your word in my heart"
    )

    // ===================
    // WORSHIP TEMPLATES
    // ===================

    val CHURCH_ATTENDANCE = HabitTemplate(
        id = "church_attendance",
        name = "Church Attendance",
        description = "Gather with fellow believers",
        category = DisciplineCategory.WORSHIP,
        iconRes = R.drawable.ic_church,
        colorRes = R.color.primary,
        frequency = Frequency.WEEKLY,
        targetType = HabitType.BOOLEAN,
        verseReference = "Hebrews 10:25"  // "Not forsaking the assembling of ourselves"
    )

    // ===================
    // REST TEMPLATES
    // ===================

    val SABBATH_REST = HabitTemplate(
        id = "sabbath_rest",
        name = "Sabbath Rest",
        description = "Honor the Lord's day with rest",
        category = DisciplineCategory.REST,
        iconRes = R.drawable.ic_sabbath,
        colorRes = R.color.accent_gold,
        frequency = Frequency.WEEKLY,
        targetType = HabitType.BOOLEAN,
        verseReference = "Exodus 20:8"  // "Remember the Sabbath day"
    )

    val FASTING = HabitTemplate(
        id = "fasting",
        name = "Fasting",
        description = "Spiritual discipline through self-denial",
        category = DisciplineCategory.REST,
        iconRes = R.drawable.ic_fasting,
        colorRes = R.color.secondary_sage,
        frequency = Frequency.CUSTOM,
        targetType = HabitType.BOOLEAN,
        verseReference = "Matthew 6:17-18"  // "When you fast..."
    )

    // ===================
    // GENEROSITY TEMPLATES
    // ===================

    val TITHE_GIVING = HabitTemplate(
        id = "tithe_giving",
        name = "Tithe/Giving",
        description = "Give generously and cheerfully",
        category = DisciplineCategory.GENEROSITY,
        iconRes = R.drawable.ic_giving,
        colorRes = R.color.streak_gold,
        frequency = Frequency.WEEKLY,
        targetType = HabitType.BOOLEAN,
        verseReference = "2 Corinthians 9:7"  // "God loves a cheerful giver"
    )

    // ===================
    // TEMPLATE COLLECTIONS
    // ===================

    /**
     * All available templates
     */
    val ALL: List<HabitTemplate> = listOf(
        MORNING_PRAYER,
        SCRIPTURE_READING,
        GRATITUDE_JOURNAL,
        CHURCH_ATTENDANCE,
        EVENING_PRAYER,
        CHRISTIAN_MEDITATION,
        FASTING,
        TITHE_GIVING,
        SABBATH_REST,
        SCRIPTURE_MEMORIZATION
    )

    /**
     * Free tier templates (3)
     */
    val FREE: List<HabitTemplate> = listOf(
        MORNING_PRAYER,
        SCRIPTURE_READING,
        GRATITUDE_JOURNAL
    )

    /**
     * Premium-only templates
     */
    val PREMIUM: List<HabitTemplate> = ALL.filter { it !in FREE }

    /**
     * Get templates by category
     */
    fun byCategory(category: DisciplineCategory): List<HabitTemplate> {
        return ALL.filter { it.category == category }
    }

    /**
     * Get template by ID
     */
    fun findById(id: String): HabitTemplate? {
        return ALL.find { it.id == id }
    }

    /**
     * Get recommended starter templates for new users
     */
    val STARTER_PACK: List<HabitTemplate> = listOf(
        MORNING_PRAYER,
        SCRIPTURE_READING,
        GRATITUDE_JOURNAL
    )

    /**
     * Get templates ordered by popularity/recommendation
     */
    val RECOMMENDED: List<HabitTemplate> = listOf(
        MORNING_PRAYER,
        SCRIPTURE_READING,
        GRATITUDE_JOURNAL,
        CHURCH_ATTENDANCE,
        CHRISTIAN_MEDITATION
    )
}
