package com.dailydevotion.app.core.models

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.Date

/**
 * Core data models for DailyDevotion.
 *
 * These extend/modify the Loop Habit Tracker models with faith-specific fields.
 */

// ===================
// ENUMS
// ===================

/**
 * Spiritual discipline categories for habits.
 */
enum class DisciplineCategory(val displayName: String, val colorRes: Int) {
    PRAYER("Prayer", R.color.prayer_purple),
    SCRIPTURE("Scripture", R.color.scripture_blue),
    WORSHIP("Worship", R.color.worship_gold),
    SERVICE("Service", R.color.service_teal),
    REST("Rest", R.color.rest_lavender),
    GENEROSITY("Generosity", R.color.generosity_amber),
    CUSTOM("Custom", R.color.primary)
}

/**
 * How often a habit should be performed.
 */
enum class Frequency {
    DAILY,
    WEEKLY,
    CUSTOM
}

/**
 * Type of habit tracking.
 */
enum class HabitType {
    BOOLEAN,  // Yes/No (did you do it?)
    NUMERIC   // Measurable (how much/how long?)
}

// ===================
// ENTITIES
// ===================

/**
 * Main Habit entity.
 *
 * Extends Loop's Habit model with:
 * - DisciplineCategory for faith organization
 * - templateId to track origin
 * - verseReference for habit-specific scripture
 */
@Entity(tableName = "habits")
data class Habit(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,

    val name: String,
    val description: String = "",

    val frequency: Frequency = Frequency.DAILY,
    val targetValue: Int = 1,
    val targetType: HabitType = HabitType.BOOLEAN,
    val unit: String = "",

    val color: Int,
    val icon: Int,

    val reminderTime: String? = null,  // Format: "HH:mm"
    val reminderDays: Int = 127,       // Bitmask for days (1=Sun, 2=Mon, etc.)

    val createdAt: Long = System.currentTimeMillis(),
    val archivedAt: Long? = null,
    val position: Int = 0,

    // DailyDevotion-specific fields
    val category: DisciplineCategory = DisciplineCategory.CUSTOM,
    val templateId: String? = null,
    val verseReference: String? = null
) {
    val isArchived: Boolean
        get() = archivedAt != null

    val isFromTemplate: Boolean
        get() = templateId != null
}

/**
 * Record of a habit completion.
 */
@Entity(tableName = "completions")
data class Completion(
    @PrimaryKey(autoGenerate = true)
    val id: Long = 0,

    val habitId: Long,
    val timestamp: Long = System.currentTimeMillis(),
    val value: Int = 1,  // For boolean: 1=done, for numeric: the amount

    // Date components for efficient querying
    val year: Int,
    val month: Int,
    val day: Int
)

/**
 * User's streak information for a habit.
 */
data class Streak(
    val habitId: Long,
    val currentStreak: Int,
    val longestStreak: Int,
    val lastCompletedDate: Date?,
    val totalCompletions: Int
)

/**
 * User preferences and settings.
 */
data class UserPreferences(
    val darkModeEnabled: Boolean = false,
    val notificationsEnabled: Boolean = true,
    val verseNotificationEnabled: Boolean = true,
    val verseNotificationTime: String = "07:00",
    val preferredTranslation: String = "WEB",
    val quietHoursStart: String? = null,  // Format: "HH:mm"
    val quietHoursEnd: String? = null,
    val firstDayOfWeek: Int = 1,  // 1=Sunday, 2=Monday
    val showStreakInNotifications: Boolean = true
)

/**
 * Premium subscription status.
 */
data class PremiumStatus(
    val isPremium: Boolean = false,
    val subscriptionType: String? = null,  // "monthly", "yearly", "lifetime"
    val expirationDate: Date? = null,
    val isInTrial: Boolean = false,
    val trialEndDate: Date? = null
) {
    val isActive: Boolean
        get() = isPremium || (isInTrial && trialEndDate?.after(Date()) == true)

    val daysUntilExpiration: Int?
        get() {
            val expDate = if (isInTrial) trialEndDate else expirationDate
            expDate ?: return null
            val diff = expDate.time - System.currentTimeMillis()
            return (diff / (1000 * 60 * 60 * 24)).toInt()
        }
}

// ===================
// VIEW MODELS
// ===================

/**
 * Habit with its current streak info for display.
 */
data class HabitWithStreak(
    val habit: Habit,
    val streak: Streak,
    val isCompletedToday: Boolean,
    val completionRateWeek: Float,
    val completionRateMonth: Float
)

/**
 * Statistics summary for display.
 */
data class StatsSummary(
    val totalHabits: Int,
    val activeHabits: Int,
    val totalCompletionsAllTime: Int,
    val totalCompletionsThisWeek: Int,
    val totalCompletionsThisMonth: Int,
    val overallCompletionRate: Float,
    val longestStreakEver: Int,
    val currentLongestStreak: Int,
    val habitsByCategory: Map<DisciplineCategory, Int>
)

/**
 * Milestone achievement for streak celebrations.
 */
data class Milestone(
    val days: Int,
    val title: String,
    val message: String,
    val achievedAt: Date?,
    val habitId: Long
)

// ===================
// CONSTANTS
// ===================

object Constants {
    const val FREE_HABIT_LIMIT = 5
    const val MAX_HABIT_NAME_LENGTH = 50
    const val MAX_DESCRIPTION_LENGTH = 200

    val MILESTONE_DAYS = listOf(3, 7, 14, 21, 30, 60, 90, 100, 180, 365)

    const val DEFAULT_REMINDER_HOUR = 8
    const val DEFAULT_REMINDER_MINUTE = 0
}
