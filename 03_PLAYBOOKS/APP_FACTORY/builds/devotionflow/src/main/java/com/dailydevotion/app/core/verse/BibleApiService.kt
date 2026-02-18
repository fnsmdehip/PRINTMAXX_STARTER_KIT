package com.dailydevotion.app.core.verse

import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

/**
 * Retrofit service for Bible API integration.
 *
 * Uses bible-api.com (free, public domain translations)
 * Supports KJV, WEB, and other public domain translations.
 */
interface BibleApiService {

    /**
     * Get a specific verse by reference
     * Example: "John 3:16", "Psalm 23:1-6"
     */
    @GET("{reference}")
    suspend fun getVerse(
        @Path("reference") reference: String,
        @Query("translation") translation: String = "web"
    ): VerseResponse

    /**
     * Get a random verse
     * Note: bible-api.com doesn't have random endpoint,
     * so we implement this client-side with a verse pool
     */
    companion object {
        const val BASE_URL = "https://bible-api.com/"
    }
}

/**
 * Response from Bible API
 */
data class VerseResponse(
    val reference: String,
    val verses: List<VerseItem>,
    val text: String,
    val translation_id: String,
    val translation_name: String,
    val translation_note: String
)

/**
 * Individual verse within a passage
 */
data class VerseItem(
    val book_id: String,
    val book_name: String,
    val chapter: Int,
    val verse: Int,
    val text: String
)

/**
 * Simplified verse model for app use
 */
data class DailyVerse(
    val reference: String,
    val text: String,
    val translation: String,
    val date: String,
    val cachedAt: Long = System.currentTimeMillis()
) {
    /**
     * Check if cache is still fresh (within 24 hours)
     */
    fun isFresh(): Boolean {
        val oneDayMs = 24 * 60 * 60 * 1000
        return System.currentTimeMillis() - cachedAt < oneDayMs
    }

    /**
     * Get shortened text for widgets/notifications (max 100 chars)
     */
    fun shortText(maxLength: Int = 100): String {
        return if (text.length <= maxLength) {
            text
        } else {
            text.take(maxLength - 3) + "..."
        }
    }
}
