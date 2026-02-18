/**
 * Android App Blocker Native Module
 *
 * This file provides the skeleton for implementing app blocking on Android.
 * Requires the following permissions in AndroidManifest.xml:
 * - PACKAGE_USAGE_STATS (to detect foreground app)
 * - SYSTEM_ALERT_WINDOW (to show blocking overlay)
 * - FOREGROUND_SERVICE (to run background monitoring)
 *
 * And optionally:
 * - Accessibility Service (for more reliable detection)
 */

package com.prayerlock

import android.app.AppOpsManager
import android.app.usage.UsageStatsManager
import android.content.Context
import android.content.Intent
import android.content.pm.ApplicationInfo
import android.content.pm.PackageManager
import android.graphics.PixelFormat
import android.os.Build
import android.os.Process
import android.provider.Settings
import android.view.LayoutInflater
import android.view.View
import android.view.WindowManager
import com.facebook.react.bridge.*
import java.util.*

class AppBlockerModule(reactContext: ReactApplicationContext) :
    ReactContextBaseJavaModule(reactContext) {

    private var blockedPackages: MutableSet<String> = mutableSetOf()
    private var overlayView: View? = null
    private var isMonitoring = false

    override fun getName(): String = "AppBlocker"

    // MARK: - Permissions

    /**
     * Request all required permissions
     * Returns true if all permissions granted
     */
    @ReactMethod
    fun requestPermissions(promise: Promise) {
        val context = reactApplicationContext

        // Check Usage Stats permission
        if (!hasUsageStatsPermission()) {
            val intent = Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS)
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK
            context.startActivity(intent)
        }

        // Check Overlay permission
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M && !Settings.canDrawOverlays(context)) {
            val intent = Intent(
                Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                android.net.Uri.parse("package:${context.packageName}")
            )
            intent.flags = Intent.FLAG_ACTIVITY_NEW_TASK
            context.startActivity(intent)
        }

        promise.resolve(true)
    }

    /**
     * Check if all required permissions are granted
     */
    @ReactMethod
    fun checkPermissions(promise: Promise) {
        val hasUsageStats = hasUsageStatsPermission()
        val hasOverlay = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            Settings.canDrawOverlays(reactApplicationContext)
        } else {
            true
        }

        promise.resolve(hasUsageStats && hasOverlay)
    }

    private fun hasUsageStatsPermission(): Boolean {
        val context = reactApplicationContext
        val appOps = context.getSystemService(Context.APP_OPS_SERVICE) as AppOpsManager

        val mode = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            appOps.unsafeCheckOpNoThrow(
                AppOpsManager.OPSTR_GET_USAGE_STATS,
                Process.myUid(),
                context.packageName
            )
        } else {
            @Suppress("DEPRECATION")
            appOps.checkOpNoThrow(
                AppOpsManager.OPSTR_GET_USAGE_STATS,
                Process.myUid(),
                context.packageName
            )
        }

        return mode == AppOpsManager.MODE_ALLOWED
    }

    // MARK: - App Discovery

    /**
     * Get list of installed apps
     * Returns array of {packageName, appName, category}
     */
    @ReactMethod
    fun getInstalledApps(promise: Promise) {
        try {
            val pm = reactApplicationContext.packageManager
            val apps = pm.getInstalledApplications(PackageManager.GET_META_DATA)

            val result = WritableNativeArray()

            for (app in apps) {
                // Skip system apps
                if (app.flags and ApplicationInfo.FLAG_SYSTEM != 0) continue

                val appInfo = WritableNativeMap().apply {
                    putString("packageName", app.packageName)
                    putString("appName", pm.getApplicationLabel(app).toString())
                    putString("category", categorizeApp(app.packageName))
                }
                result.pushMap(appInfo)
            }

            promise.resolve(result)
        } catch (e: Exception) {
            promise.reject("GET_APPS_ERROR", e.message)
        }
    }

    private fun categorizeApp(packageName: String): String {
        return when {
            packageName.contains("facebook") ||
            packageName.contains("instagram") ||
            packageName.contains("twitter") ||
            packageName.contains("tiktok") ||
            packageName.contains("snapchat") ||
            packageName.contains("reddit") -> "social"

            packageName.contains("game") ||
            packageName.contains("puzzle") -> "game"

            packageName.contains("youtube") ||
            packageName.contains("netflix") ||
            packageName.contains("spotify") -> "entertainment"

            else -> "other"
        }
    }

    // MARK: - Blocking

    /**
     * Set apps to block
     */
    @ReactMethod
    fun blockApps(packages: ReadableArray, promise: Promise) {
        blockedPackages.clear()
        for (i in 0 until packages.size()) {
            packages.getString(i)?.let { blockedPackages.add(it) }
        }

        if (!isMonitoring) {
            startMonitoring()
        }

        promise.resolve(true)
    }

    /**
     * Unblock all apps
     */
    @ReactMethod
    fun unblockApps(promise: Promise) {
        blockedPackages.clear()
        stopMonitoring()
        hideOverlay()
        promise.resolve(true)
    }

    /**
     * Check if apps are currently blocked
     */
    @ReactMethod
    fun isBlocking(promise: Promise) {
        promise.resolve(blockedPackages.isNotEmpty() && isMonitoring)
    }

    // MARK: - Monitoring

    private fun startMonitoring() {
        isMonitoring = true

        // Start a foreground service that checks foreground app
        // and shows overlay when blocked app is detected

        // TODO: Implement ForegroundService that:
        // 1. Polls UsageStatsManager every second
        // 2. Checks if foreground app is in blockedPackages
        // 3. Shows overlay if blocked app detected
        // 4. Hides overlay when PrayerLock is foreground

        // Alternative: Use AccessibilityService for more reliable detection
    }

    private fun stopMonitoring() {
        isMonitoring = false
        // Stop foreground service
    }

    /**
     * Get the currently active app
     */
    private fun getForegroundApp(): String? {
        val usm = reactApplicationContext.getSystemService(Context.USAGE_STATS_SERVICE)
            as UsageStatsManager

        val now = System.currentTimeMillis()
        val stats = usm.queryUsageStats(
            UsageStatsManager.INTERVAL_DAILY,
            now - 10000,
            now
        )

        if (stats.isNullOrEmpty()) return null

        return stats.maxByOrNull { it.lastTimeUsed }?.packageName
    }

    // MARK: - Overlay

    private fun showOverlay() {
        val activity = currentActivity ?: return

        activity.runOnUiThread {
            if (overlayView != null) return@runOnUiThread

            val windowManager = activity.getSystemService(Context.WINDOW_SERVICE)
                as WindowManager

            // Create overlay view
            // TODO: Inflate a custom layout with:
            // - "Complete your devotion to unlock" message
            // - PrayerLock logo
            // - "Open PrayerLock" button

            val params = WindowManager.LayoutParams(
                WindowManager.LayoutParams.MATCH_PARENT,
                WindowManager.LayoutParams.MATCH_PARENT,
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY
                } else {
                    @Suppress("DEPRECATION")
                    WindowManager.LayoutParams.TYPE_PHONE
                },
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE or
                    WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL or
                    WindowManager.LayoutParams.FLAG_LAYOUT_IN_SCREEN,
                PixelFormat.TRANSLUCENT
            )

            // TODO: Create and add overlay view
            // overlayView = LayoutInflater.from(activity).inflate(...)
            // windowManager.addView(overlayView, params)
        }
    }

    private fun hideOverlay() {
        val activity = currentActivity ?: return

        activity.runOnUiThread {
            overlayView?.let {
                val windowManager = activity.getSystemService(Context.WINDOW_SERVICE)
                    as WindowManager
                windowManager.removeView(it)
                overlayView = null
            }
        }
    }
}

/**
 * React Native Package Registration
 *
 * Add to MainApplication.java:
 *
 * @Override
 * protected List<ReactPackage> getPackages() {
 *     return Arrays.<ReactPackage>asList(
 *         new MainReactPackage(),
 *         new AppBlockerPackage() // Add this
 *     );
 * }
 *
 * Create AppBlockerPackage.kt:
 *
 * class AppBlockerPackage : ReactPackage {
 *     override fun createNativeModules(reactContext: ReactApplicationContext) =
 *         listOf(AppBlockerModule(reactContext))
 *
 *     override fun createViewManagers(reactContext: ReactApplicationContext) =
 *         emptyList<ViewManager<*, *>>()
 * }
 */
