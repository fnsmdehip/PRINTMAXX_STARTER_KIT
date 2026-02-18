package com.dailydevotion.app.core.mascot

import kotlin.random.Random

/**
 * Dove mascot messages and personality.
 *
 * The dove represents peace and the Holy Spirit.
 * Messages are faith-focused, encouraging, and avoid religious cliches.
 * All messages should feel supportive, not preachy.
 */
object DoveMascot {

    /**
     * Greeting messages shown on app open
     */
    val GREETINGS = listOf(
        "Peace be with you today.",
        "Ready to grow in faith?",
        "Let's walk together in the Spirit.",
        "God's grace is new every morning.",
        "Another day, another opportunity to grow.",
        "Welcome back to your spiritual journey.",
        "The Lord is with you today.",
        "Let's build holy habits together.",
        "Grace and peace to you.",
        "Ready for today's devotion?"
    )

    /**
     * Messages when user completes a habit
     */
    val COMPLETION_MESSAGES = listOf(
        "Well done!",
        "You've honored God today.",
        "Another step in your journey.",
        "Faithfulness looks good on you.",
        "Heaven rejoices with you.",
        "Keep pressing on.",
        "You're building something beautiful.",
        "God sees your faithfulness.",
        "Small steps, big impact.",
        "Consistency is the key."
    )

    /**
     * Encouragement messages when user misses a habit
     */
    val ENCOURAGEMENTS = listOf(
        "His mercies are new every morning.",
        "Don't give up. You're growing.",
        "Tomorrow is a new opportunity.",
        "Grace covers yesterday.",
        "Pick up where you left off.",
        "Progress, not perfection.",
        "God's not keeping score. Neither should you.",
        "Rest, then restart.",
        "Every day is a fresh start.",
        "You're still on the path."
    )

    /**
     * Streak milestone celebrations
     */
    val STREAK_CELEBRATIONS = mapOf(
        3 to "Three days of faithfulness! You're building momentum.",
        7 to "One week strong! Keep pressing on.",
        14 to "Two weeks! Holy habits are forming.",
        21 to "21 days! They say that's when habits stick.",
        30 to "A month of devotion! What an accomplishment.",
        60 to "Two months! Your dedication inspires.",
        90 to "90 days of faithfulness! This is transformation.",
        100 to "100 days! A century of devotion.",
        180 to "Half a year! Imagine where you'll be in another six months.",
        365 to "One full year! What an incredible journey of faith."
    )

    /**
     * Messages for prayer habits specifically
     */
    val PRAYER_MESSAGES = listOf(
        "Come boldly to the throne of grace.",
        "He hears you.",
        "Prayer changes things.",
        "Conversation with the Creator.",
        "Talk to your Father.",
        "He's listening."
    )

    /**
     * Messages for scripture habits
     */
    val SCRIPTURE_MESSAGES = listOf(
        "Thy word is a lamp unto my feet.",
        "Feast on the Word.",
        "Let it transform your mind.",
        "Hidden in your heart.",
        "Living and active.",
        "Breathed out by God."
    )

    /**
     * Messages for gratitude habits
     */
    val GRATITUDE_MESSAGES = listOf(
        "Count your blessings.",
        "A thankful heart sees clearly.",
        "Gratitude changes everything.",
        "Give thanks in all circumstances.",
        "What are you grateful for today?",
        "Notice the small things."
    )

    /**
     * Night/evening messages
     */
    val EVENING_MESSAGES = listOf(
        "Rest well. Tomorrow is a gift.",
        "In peace I will lie down and sleep.",
        "End the day in gratitude.",
        "His faithfulness continues through the night.",
        "Sleep in peace.",
        "Tomorrow's mercies await."
    )

    // ===================
    // HELPER METHODS
    // ===================

    /**
     * Get a random greeting message
     */
    fun getGreeting(): String = GREETINGS.random()

    /**
     * Get a random completion message
     */
    fun getCompletionMessage(): String = COMPLETION_MESSAGES.random()

    /**
     * Get a random encouragement message
     */
    fun getEncouragement(): String = ENCOURAGEMENTS.random()

    /**
     * Get streak celebration message, or null if not a milestone
     */
    fun getStreakCelebration(streakDays: Int): String? {
        return STREAK_CELEBRATIONS[streakDays]
    }

    /**
     * Get the next streak milestone
     */
    fun getNextMilestone(currentStreak: Int): Int {
        return STREAK_CELEBRATIONS.keys
            .filter { it > currentStreak }
            .minOrNull() ?: 365
    }

    /**
     * Get context-appropriate message based on habit type
     */
    fun getHabitMessage(habitType: HabitType): String {
        return when (habitType) {
            HabitType.PRAYER -> PRAYER_MESSAGES.random()
            HabitType.SCRIPTURE -> SCRIPTURE_MESSAGES.random()
            HabitType.GRATITUDE -> GRATITUDE_MESSAGES.random()
            else -> COMPLETION_MESSAGES.random()
        }
    }

    /**
     * Get time-appropriate message
     */
    fun getTimeBasedGreeting(hour: Int): String {
        return when {
            hour < 12 -> "Good morning! ${GREETINGS.random()}"
            hour < 17 -> "Good afternoon! ${GREETINGS.random()}"
            else -> EVENING_MESSAGES.random()
        }
    }

    /**
     * Get message for when user returns after absence
     */
    fun getReturnMessage(daysAway: Int): String {
        return when {
            daysAway == 1 -> "Welcome back! Ready to continue?"
            daysAway <= 3 -> "You've been missed. Let's pick up where we left off."
            daysAway <= 7 -> "It's good to see you again. Grace covers every absence."
            else -> "Welcome back! Today is a new beginning."
        }
    }

    /**
     * Habit types for context-aware messages
     */
    enum class HabitType {
        PRAYER,
        SCRIPTURE,
        GRATITUDE,
        WORSHIP,
        SERVICE,
        REST,
        GENEROSITY,
        OTHER
    }
}
