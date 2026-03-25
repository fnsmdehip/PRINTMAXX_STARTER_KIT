/**
 * Ad service - REMOVED.
 *
 * AdMob has been removed to simplify App Store compliance.
 * Revenue model is subscription-only via RevenueCat.
 * All functions are safe no-ops for backward compatibility.
 */

export function loadInterstitialAd(): void {}
export function showInterstitialAd(): boolean { return false; }
export function isInterstitialReady(): boolean { return false; }
export function loadRewardedAd(): void {}
export function showRewardedAd(): Promise<boolean> { return Promise.resolve(false); }
export function isRewardedReady(): boolean { return false; }
export function preloadAllAds(): void {}
export function shouldShowInterstitial(_totalScans: number): boolean { return false; }
