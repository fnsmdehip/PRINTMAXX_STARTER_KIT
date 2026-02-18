package com.dailydevotion.app.core.templates

import com.dailydevotion.app.core.models.DisciplineCategory
import com.dailydevotion.app.core.models.Frequency
import com.dailydevotion.app.core.models.HabitType

/**
 * Data class representing a pre-built habit template.
 * Templates allow users to quickly create common spiritual discipline habits
 * with sensible defaults.
 */
data class HabitTemplate(
    val id: String,
    val name: String,
    val description: String,
    val category: DisciplineCategory,
    val iconRes: Int,
    val colorRes: Int,
    val frequency: Frequency,
    val targetType: HabitType,
    val targetValue: Int = 1,
    val unit: String = "",
    val reminderTime: String? = null,
    val verseReference: String? = null  // Optional scripture for this habit
) {

    /**
     * Convert template to a new Habit instance
     */
    fun toHabit(): Habit {
        return Habit(
            id = 0,  // New habit, DB will assign ID
            name = name,
            description = description,
            frequency = frequency,
            targetValue = targetValue,
            targetType = targetType,
            color = colorRes,
            icon = iconRes,
            reminderTime = reminderTime,
            createdAt = System.currentTimeMillis(),
            category = category,
            templateId = id,
            verseReference = verseReference
        )
    }

    companion object {
        /**
         * Check if a habit was created from a template
         */
        fun isFromTemplate(habit: Habit): Boolean {
            return habit.templateId != null
        }
    }
}
