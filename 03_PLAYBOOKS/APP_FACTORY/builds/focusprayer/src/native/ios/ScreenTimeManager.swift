/**
 * iOS Screen Time API Native Module
 *
 * This file provides the skeleton for implementing Screen Time API integration.
 * Requires iOS 15+ and the following capabilities enabled in Xcode:
 * - FamilyControls
 * - ManagedSettings
 * - DeviceActivity
 *
 * IMPORTANT: Screen Time API requires Apple approval.
 * Submit a request at: https://developer.apple.com/contact/request/family-controls-distribution
 */

import Foundation
import FamilyControls
import ManagedSettings
import DeviceActivity

@objc(ScreenTimeManager)
class ScreenTimeManager: NSObject {

    private let store = ManagedSettingsStore()
    private var selectedApps: Set<ApplicationToken> = []

    // MARK: - Authorization

    /**
     * Request authorization to use Screen Time API
     * User will see a system prompt to grant access
     */
    @objc
    func requestAuthorization(_ resolve: @escaping RCTPromiseResolveBlock,
                              reject: @escaping RCTPromiseRejectBlock) {
        Task {
            do {
                try await AuthorizationCenter.shared.requestAuthorization(for: .individual)
                resolve(true)
            } catch {
                reject("AUTH_ERROR", "Failed to get Screen Time authorization: \(error.localizedDescription)", error)
            }
        }
    }

    /**
     * Check if authorization has been granted
     */
    @objc
    func checkAuthorization(_ resolve: @escaping RCTPromiseResolveBlock,
                            reject: @escaping RCTPromiseRejectBlock) {
        let status = AuthorizationCenter.shared.authorizationStatus
        resolve(status == .approved)
    }

    // MARK: - App Selection

    /**
     * Show the FamilyActivityPicker for user to select apps to block
     * Note: iOS does not allow programmatic access to installed apps list
     * Users must select apps through the system picker
     */
    @objc
    func presentAppPicker(_ resolve: @escaping RCTPromiseResolveBlock,
                          reject: @escaping RCTPromiseRejectBlock) {
        // FamilyActivityPicker must be presented via SwiftUI
        // This requires a bridging view controller
        // See: https://developer.apple.com/documentation/familycontrols/familyactivitypicker

        // TODO: Implement SwiftUI bridge to present picker
        // Store selected apps in self.selectedApps
        resolve(true)
    }

    // MARK: - Blocking

    /**
     * Block the selected apps
     * Creates a shield that prevents app launch
     */
    @objc
    func blockApps(_ resolve: @escaping RCTPromiseResolveBlock,
                   reject: @escaping RCTPromiseRejectBlock) {
        guard !selectedApps.isEmpty else {
            reject("NO_APPS", "No apps selected to block", nil)
            return
        }

        // Apply shield to selected apps
        store.shield.applications = selectedApps

        // Optional: Customize shield appearance
        // store.shield.applicationCategories = ...
        // store.shield.webDomains = ...

        resolve(true)
    }

    /**
     * Unblock all apps
     * Removes the shield allowing normal app access
     */
    @objc
    func unblockApps(_ resolve: @escaping RCTPromiseResolveBlock,
                     reject: @escaping RCTPromiseRejectBlock) {
        store.shield.applications = nil
        resolve(true)
    }

    /**
     * Check if apps are currently blocked
     */
    @objc
    func isBlocking(_ resolve: @escaping RCTPromiseResolveBlock,
                    reject: @escaping RCTPromiseRejectBlock) {
        let isBlocking = store.shield.applications != nil
        resolve(isBlocking)
    }

    // MARK: - Device Activity Monitoring (Optional)

    /**
     * Start monitoring device activity
     * Can track screen time and app usage
     */
    @objc
    func startMonitoring(_ resolve: @escaping RCTPromiseResolveBlock,
                         reject: @escaping RCTPromiseRejectBlock) {
        // DeviceActivityMonitor can be used to:
        // - Track when user opens blocked apps
        // - Trigger actions at specific times
        // - Monitor total screen time

        // TODO: Implement DeviceActivitySchedule
        resolve(true)
    }

    // MARK: - React Native Bridge Methods

    @objc
    static func requiresMainQueueSetup() -> Bool {
        return false
    }

    @objc
    static func moduleName() -> String! {
        return "ScreenTimeManager"
    }
}

// MARK: - React Native Bridge

/**
 * Bridge macro for React Native
 * Create a file ScreenTimeManager.m with:
 *
 * #import <React/RCTBridgeModule.h>
 *
 * @interface RCT_EXTERN_MODULE(ScreenTimeManager, NSObject)
 *
 * RCT_EXTERN_METHOD(requestAuthorization:(RCTPromiseResolveBlock)resolve
 *                   reject:(RCTPromiseRejectBlock)reject)
 *
 * RCT_EXTERN_METHOD(checkAuthorization:(RCTPromiseResolveBlock)resolve
 *                   reject:(RCTPromiseRejectBlock)reject)
 *
 * RCT_EXTERN_METHOD(presentAppPicker:(RCTPromiseResolveBlock)resolve
 *                   reject:(RCTPromiseRejectBlock)reject)
 *
 * RCT_EXTERN_METHOD(blockApps:(RCTPromiseResolveBlock)resolve
 *                   reject:(RCTPromiseRejectBlock)reject)
 *
 * RCT_EXTERN_METHOD(unblockApps:(RCTPromiseResolveBlock)resolve
 *                   reject:(RCTPromiseRejectBlock)reject)
 *
 * RCT_EXTERN_METHOD(isBlocking:(RCTPromiseResolveBlock)resolve
 *                   reject:(RCTPromiseRejectBlock)reject)
 *
 * @end
 */
