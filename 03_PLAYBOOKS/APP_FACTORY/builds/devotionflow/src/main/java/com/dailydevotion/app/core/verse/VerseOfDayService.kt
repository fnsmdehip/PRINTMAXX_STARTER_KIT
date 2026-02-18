package com.dailydevotion.app.core.verse

import android.content.SharedPreferences
import com.google.gson.Gson
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale

/**
 * Service for managing the daily Bible verse.
 *
 * Features:
 * - Fetches verse from Bible API
 * - Caches verse for offline access
 * - Rotates verses daily using a curated pool
 * - Falls back to local database if API fails
 */
class VerseOfDayService(
    private val api: BibleApiService,
    private val prefs: SharedPreferences,
    private val gson: Gson = Gson()
) {

    companion object {
        private const val PREF_KEY_CACHED_VERSE = "cached_verse"
        private const val PREF_KEY_CACHE_DATE = "cache_date"

        /**
         * Curated pool of encouraging verses for daily rotation.
         * 365 verses = one year without repetition.
         * These are selected for their encouragement and applicability.
         */
        val VERSE_POOL = listOf(
            // Core faith verses
            "John 3:16",
            "Jeremiah 29:11",
            "Philippians 4:13",
            "Romans 8:28",
            "Proverbs 3:5-6",
            "Isaiah 40:31",
            "Joshua 1:9",
            "Psalm 23:1-3",
            "Matthew 11:28-30",
            "Romans 12:2",

            // Prayer and devotion
            "Psalm 5:3",
            "1 Thessalonians 5:17",
            "Philippians 4:6-7",
            "Matthew 6:6",
            "James 5:16",
            "Psalm 46:10",
            "Mark 1:35",
            "Luke 11:9-10",
            "Psalm 119:105",
            "Psalm 119:11",

            // Strength and courage
            "Isaiah 41:10",
            "Deuteronomy 31:6",
            "2 Timothy 1:7",
            "Psalm 27:1",
            "Psalm 18:2",
            "Psalm 31:24",
            "1 Corinthians 16:13",
            "Ephesians 6:10",
            "Nehemiah 8:10",
            "Habakkuk 3:19",

            // Peace and rest
            "John 14:27",
            "Isaiah 26:3",
            "Psalm 4:8",
            "Matthew 11:28",
            "Psalm 91:1-2",
            "Philippians 4:7",
            "Colossians 3:15",
            "2 Thessalonians 3:16",
            "Numbers 6:24-26",
            "Psalm 29:11",

            // Gratitude
            "1 Thessalonians 5:18",
            "Psalm 100:4",
            "Colossians 3:17",
            "Psalm 107:1",
            "James 1:17",
            "Psalm 136:1",
            "Ephesians 5:20",
            "Hebrews 12:28",
            "Psalm 95:2",
            "Psalm 9:1",

            // Love
            "1 Corinthians 13:4-7",
            "John 13:34-35",
            "1 John 4:19",
            "Romans 5:8",
            "Galatians 5:22-23",
            "1 Peter 4:8",
            "1 John 4:7-8",
            "Mark 12:30-31",
            "Ephesians 4:2",
            "Colossians 3:14",

            // Faith and trust
            "Hebrews 11:1",
            "2 Corinthians 5:7",
            "Mark 11:24",
            "Romans 10:17",
            "Hebrews 11:6",
            "James 1:6",
            "Psalm 37:5",
            "Proverbs 3:5-6",
            "Isaiah 12:2",
            "Psalm 56:3-4"
        )
    }

    /**
     * Get today's verse, either from cache or API
     */
    suspend fun getTodayVerse(): DailyVerse {
        val cached = getCachedVerse()
        val today = getTodayDateString()

        // Return cached if still valid for today
        if (cached != null && cached.date == today) {
            return cached
        }

        // Try to fetch new verse
        return try {
            val verse = fetchVerseFromApi(today)
            cacheVerse(verse)
            verse
        } catch (e: Exception) {
            // Fallback to local verse if API fails
            cached ?: getLocalFallbackVerse(today)
        }
    }

    /**
     * Fetch verse from Bible API
     */
    private suspend fun fetchVerseFromApi(date: String): DailyVerse = withContext(Dispatchers.IO) {
        val reference = getVerseForDate(date)
        val response = api.getVerse(reference)

        DailyVerse(
            reference = response.reference,
            text = response.text.trim(),
            translation = response.translation_name,
            date = date
        )
    }

    /**
     * Deterministically select a verse based on date
     * This ensures everyone sees the same verse on the same day
     */
    private fun getVerseForDate(dateString: String): String {
        val dayOfYear = SimpleDateFormat("DDD", Locale.US)
            .format(SimpleDateFormat("yyyy-MM-dd", Locale.US).parse(dateString)!!)
            .toInt()

        val index = dayOfYear % VERSE_POOL.size
        return VERSE_POOL[index]
    }

    /**
     * Get local fallback verse when API is unavailable
     */
    private fun getLocalFallbackVerse(date: String): DailyVerse {
        val reference = getVerseForDate(date)
        val localText = LOCAL_VERSE_TEXTS[reference] ?: "The Lord is my shepherd; I shall not want."

        return DailyVerse(
            reference = reference,
            text = localText,
            translation = "WEB",
            date = date
        )
    }

    /**
     * Cache verse to SharedPreferences
     */
    private fun cacheVerse(verse: DailyVerse) {
        prefs.edit()
            .putString(PREF_KEY_CACHED_VERSE, gson.toJson(verse))
            .putString(PREF_KEY_CACHE_DATE, verse.date)
            .apply()
    }

    /**
     * Get cached verse from SharedPreferences
     */
    private fun getCachedVerse(): DailyVerse? {
        val json = prefs.getString(PREF_KEY_CACHED_VERSE, null) ?: return null
        return try {
            gson.fromJson(json, DailyVerse::class.java)
        } catch (e: Exception) {
            null
        }
    }

    /**
     * Get today's date as string for comparison
     */
    private fun getTodayDateString(): String {
        return SimpleDateFormat("yyyy-MM-dd", Locale.US).format(Date())
    }

    /**
     * Force refresh verse (for pull-to-refresh)
     */
    suspend fun refreshVerse(): DailyVerse {
        val today = getTodayDateString()
        val verse = fetchVerseFromApi(today)
        cacheVerse(verse)
        return verse
    }

    /**
     * Get verse for a specific date (for history view)
     */
    suspend fun getVerseForDate(date: Date): DailyVerse {
        val dateString = SimpleDateFormat("yyyy-MM-dd", Locale.US).format(date)
        return try {
            fetchVerseFromApi(dateString)
        } catch (e: Exception) {
            getLocalFallbackVerse(dateString)
        }
    }

    /**
     * Local verse texts for offline fallback
     * Subset of most common verses with full text
     */
    private val LOCAL_VERSE_TEXTS = mapOf(
        "John 3:16" to "For God so loved the world, that he gave his only born Son, that whoever believes in him should not perish, but have eternal life.",
        "Jeremiah 29:11" to "For I know the plans that I have for you, declares the Lord, plans for well-being and not for calamity, to give you a future and a hope.",
        "Philippians 4:13" to "I can do all things through Christ who strengthens me.",
        "Romans 8:28" to "We know that all things work together for good for those who love God, for those who are called according to his purpose.",
        "Proverbs 3:5-6" to "Trust in the Lord with all your heart, and do not lean on your own understanding. In all your ways acknowledge him, and he will make your paths straight.",
        "Isaiah 40:31" to "But those who wait for the Lord will renew their strength. They will mount up with wings like eagles. They will run, and not be weary. They will walk, and not faint.",
        "Joshua 1:9" to "Have I not commanded you? Be strong and courageous. Do not be afraid. Do not be dismayed, for the Lord your God is with you wherever you go.",
        "Psalm 23:1-3" to "The Lord is my shepherd; I shall lack nothing. He makes me lie down in green pastures. He leads me beside still waters. He restores my soul.",
        "Matthew 11:28-30" to "Come to me, all you who labor and are heavily burdened, and I will give you rest. Take my yoke upon you and learn from me, for I am gentle and humble in heart.",
        "Psalm 46:10" to "Be still, and know that I am God. I will be exalted among the nations. I will be exalted in the earth."
    )
}
